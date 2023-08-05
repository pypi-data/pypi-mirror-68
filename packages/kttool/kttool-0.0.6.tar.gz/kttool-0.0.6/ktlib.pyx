#cython: language_level=3, c_string_type=unicode, c_string_encoding=utf8, boundscheck=False, cdivision=True, wraparound=False
# distutils: language=c++
import sys
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport bool as bool_t
import requests
import os
import re
import time
import shutil
from bs4 import BeautifulSoup
import multiprocessing
import concurrent.futures
from reprint import output
from html.parser import HTMLParser
import emoji
from collections import namedtuple
import subprocess
from subprocess import Popen, PIPE
import json
import shlex
from resource import *
import psutil
import configparser
import webbrowser
import signal

__all__ = [
    'arg_parse',
    'color_red',
    'color_green',
    'exit_gracefully'
]

# -------------- Global varible ----------------
cdef const char* _KATTIS_RC_URL = 'https://open.kattis.com/download/kattisrc'
cdef object _HEADERS = {'User-Agent': 'kt'}
cdef const char* _VERSION = '0.0.4'
cdef const char* _PYPI_PACKAGE_INFO = 'https://pypi.org/pypi/kttool/json'
cdef list test_subprocesses = []
# global structs
PLanguage = namedtuple('ProgrammingLanguage', 
    ['alias', 'extension', 'full_name', 'pre_script', 'script', 'post_script']
)

cdef class ConfigError(Exception):
    pass

cdef object map_template_to_plang = {
    'c': PLanguage('c', 'c','C', 
        'gcc $%file%$.c -o $%file%$.out',
        './$%file%$.out',
        'rm $%file%$.out'
    ),
    'cpp': PLanguage('cpp', 'cpp', 'C++',
        'g++ -std=c++14 -D_GLIBCXX_DEBUG -D_GLIBCXX_DEBUG_PEDANTIC -O3 $%file%$.cpp -o $%file%$.out',
        './$%file%$.out',
        'rm $%file%$.out'
    ),
    'cc': PLanguage('cc', 'cc', 'C++', 
        'g++ -std=c++14 -D_GLIBCXX_DEBUG -D_GLIBCXX_DEBUG_PEDANTIC -O3 $%file%$.cc -o $%file%$.out',
        './$%file%$.out',
        'rm $%file%$.out'
    ),
    'go': PLanguage('go', 'go', 'Go', 
        'go build -o $%file%$',
        './$%file%$',
        'rm $%file%$'
    ),
    'java': PLanguage('java', 'java', 'Java', 
        'javac *.java',
        './$%file%$',
        'rm $%file%$'
    ),
    'js': PLanguage('js', 'js', 'JavaScript', 
        '',
        'node $%file%$.js',
        ''
    ),
    'rs': PLanguage('rs', 'rs', 'Rust', 
        'rustc $%file%$.rs',
        './$%file%$',
        'rm $%file%$'
    ),
    'py2': PLanguage('py2', 'py', 'Python 2', 
        '',
        'python2 $%file%$.py',
        ''
    ),
    'py3': PLanguage('py3', 'py', 'Python 3', 
        '',
        'python3 $%file%$.py',
        ''
    )
}


# -------------- Color for formatting ----------------
cdef:
    string BOLD_SEQ = b'\033[1m'
    string RESET_SEQ = b'\033[0m'
    string BLACK = b'\033[6;90m'
    string RED = b'\033[6;91m'
    string GREEN = b'\033[6;92m'
    string YELLOW = b'\033[6;93m'
    string BLUE = b'\033[6;94m'
    string MAGENTA = b'\033[6;95m'
    string CYAN = b'\033[6;96m'
    string WHITE = b'\033[6;97m'

cpdef string color_cyan(const string& text) nogil:
    cdef:
        string res = CYAN
    res.append(text)
    res.append(RESET_SEQ)
    return res

cpdef string color_green(const string& text) nogil:
    cdef:
        string res = GREEN
    res.append(text)
    res.append(RESET_SEQ)
    return res


cpdef string color_red(const string& text) nogil:
    cdef:
        string res = RED
    res.append(text)
    res.append(RESET_SEQ)
    return res

# -------------- Utility functions ----------------
cdef string ask_with_default(string qu, string default_val=b''):
    ''' Print out `qu` to console and ask for input value from user
    If no input was provided by user, `default_val` will be returned instead
    Args:
    - qu:  question to asked
    - default_val: Default value to be used
    Returns:
    - string value as the response
    '''
    cdef:
        string ret
    qu = f'Please enter {color_cyan(qu)}'
    if default_val.size() > 0:
        qu = f'{qu} | Default value: {default_val}\n'
    ret = input(qu)
    if ret.size() == 0:
        return default_val
    return ret

cdef void make_list_equal(
    vector[string]& lhs, 
    vector[string]& rhs, 
    string pad_element = b''
) nogil:
    ''' Make two vector of string equation in length by padding with `pad_element`
    Args:
    - lhs, rhs: 2 vectors of string to be made equal in length
    - pad_element: string to fill the shorter vector
    '''
    while lhs.size() < rhs.size():
        lhs.push_back(pad_element)
    while rhs.size() < lhs.size():
        rhs.push_back(pad_element)



# -------------- Core functions/classes ----------------
cdef class Action(object):
    ''' Base class for handle general command.
    Handle loading up .kattisrc config file
    '''
    def __cinit__(self):
        self.config_path = os.path.join(os.getenv('HOME'), '.kattisrc') # kattis config file
        self.kt_config = os.path.join(os.getenv('HOME'), '.ktconfig') # kt tool file

    cdef string get_url(self, const string& option, string default = b''):
        ''' Get appropriate urls from kattisrc file
        Args:
        - option: parameter to get from katticrc config file
        - default: fallback value if option is not present
        Returns:
        - Full url path to the required attr
        '''
        cdef:
            string kattis_host
        if self.cfg.has_option('kattis', option):
            return self.cfg.get('kattis', option)
        else:
            kattis_host = self.cfg.get('kattis', 'hostname')
            return f'https://{kattis_host}/{default}'


    cdef read_config_from_file(self):
        ''' kttool deals with 2 config files:
        - kattisrc: provided by official kattis website, provide domain name and general urls
        - ktconfig: handle templates by kttool
        '''
        # Initialize ktconfig file if file doesnt exist
        if not os.path.exists(self.kt_config):
            with open(self.kt_config, 'w') as f:
                f.write('{}\n')

        self.cfg = configparser.ConfigParser()
        if not os.path.exists(self.config_path):
            raise RuntimeError(f'No valid config file at {self.config_path}. '
            f'Please download it at {_KATTIS_RC_URL}')

        self.cfg.read(self.config_path)
        username = self.cfg.get('user', 'username')
        password = token = None
        try:
            password = self.cfg.get('user', 'password')
        except configparser.NoOptionError:
            pass
        try:
            token = self.cfg.get('user', 'token')
        except configparser.NoOptionError:
            pass
        if password is None and token is None:
            raise ConfigError('''\
        Your .kattisrc file appears corrupted. It must provide a token (or a
        KATTIS password).
        Please download a new .kattisrc file''')
        print(f'Username: {color_green(username)}')


    cdef login(self):
        ''' Try to login and obtain cookies from succesful signin
        '''
        cdef:
            string login_url
            string err
        username = self.cfg.get('user', 'username')
        password = token = None
        try:
            password = self.cfg.get('user', 'password')
        except configparser.NoOptionError:
            pass
        try:
            token = self.cfg.get('user', 'token')
        except configparser.NoOptionError:
            pass
        login_url = self.get_url(b'loginurl', b'login')
        login_args = {'user': username, 'script': 'true'}
        if password:
            login_args['password'] = password
        if token:
            login_args['token'] = token
        login_reply = requests.post(login_url, data=login_args, headers=_HEADERS)
        
        if not login_reply.status_code == 200:
            if login_reply.status_code == 403:
                err = b'Incorrect username or password/token (403)'
            elif login_reply.status_code == 404:
                err = b'Incorrect login URL (404)'
            else:
                err = f'Status code: {login_reply.status_code}'
            raise RuntimeError(f'Login failed. {err}')
        self.cookies = login_reply.cookies

    cdef string get_problem_id(self):
        # ASsuming user is in the folder with the name of the problem id
        return os.path.basename(os.getcwd()) 

    cdef string get_problem_url(self):
        cdef:
            string domain = f"https://{self.get_url(b'hostname')}"
            string problem_id = self.get_problem_id()

        return os.path.join(
            domain,
            'problems',
            problem_id
        )


    cdef _act(self):
        raise NotImplementedError

    def act(self):
        ''' Python wrapper function to call cython private method _act
        '''
        self.read_config_from_file()
        self._act()




cpdef void write_samples(tuple sample_data):
    ''' Write input/output sample to file. This is used for multiprocess pool to generate input/output files
    Args:
    - sample_data: a tuple representing index, string data, problem id and a boolean declaring whether current
    file is input (False if the file is output)
    '''
    cdef:
        string file_name_prefix = b'in' if sample_data[3] else b'ans'
        string file_name = f'{sample_data[2]}/{file_name_prefix}{sample_data[0]}.txt'
    
    with open(file_name, 'w') as f:
        f.write(sample_data[1])

cdef class Gen(Action):
    ''' Handle `gen` command for kt_tool '''
    def __cinit__(self, string problem_id):
        self._problem_id = problem_id
        

    cdef _gen_samples(self):
        ''' Generate sample input file for `self._problem_id`
        The basic flow is to scrape the problem task page and retrieve the relevent fields
        Generate the sample files to problem id folder
        For example, if the problem id is distinctivecharacter, `kt gen` will
        - Generate a folder called distinctivecharacter
        - Get sample intput, output from problem task page and generate to distinctivecharacter/, in this
        example there will be 4 files generated
        + distinctivecharacter/in1.txt
        + distinctivecharacter/ans1.txt
        + distinctivecharacter/in2.txt
        + distinctivecharacter/ans2.txt
        - Generate a template file (distinctivecharacter.cpp) if a template file is provided in the .ktconfig file
        '''
        cdef:
            string domain = f"https://{self.get_url(b'hostname')}"
            object template_file = {}
            list sample_data = []
            
        self.login()
        self._url = os.path.join(
            domain,
            'problems',
            self._problem_id
        )
        page = requests.get(self._url, cookies=self.cookies, headers=_HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find_all('pre')

        for i in range(len(data)):
            if i & 1:
                sample_data.append((i // 2 + 1, data[i].text, self._problem_id, False))
            else:
                sample_data.append((i // 2 + 1, data[i].text, self._problem_id, True))

        assert(len(data) % 2 == 0, 'Internal error: Number of sample input '
        ' is not equal to number of sample output')

        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            executor.map(write_samples, sample_data)

        print(color_green(f'Generate {len(sample_data) // 2} sample(s) to {self._problem_id}'))
        if not os.path.exists(self.kt_config):
            print(color_red(b'.ktconfig file has not been set up so no template was generated. '
            b'Please use `kt config` to set up a template file'))
            return

        
        with open(self.kt_config, 'r') as f:
            template_file = json.load(f)
        for k, template in template_file.items():
            if template.get('default', False):
                shutil.copyfile(template.get('path'), f'{self._problem_id}/{self._problem_id}.{map_template_to_plang[k].extension}')
                print(color_green(b'Template file has been generated'))
                return
        print(color_red(f'No default template detected in {self.kt_config}'))



    cdef _act(self):
        print(f'Problem is {self._problem_id}')
        os.makedirs(self._problem_id, exist_ok=True)
        self._gen_samples()
    

cdef bool_t compare_entity(const string& lhs, const string& rhs, string& diff) nogil:
    if lhs == rhs:
        diff.append(lhs)
        diff.push_back(b' ')
        return True
    diff.append(color_red(lhs))
    diff.append(color_green(rhs))
    diff.push_back(b' ')
    return False


cdef class Test(Action):
    cdef detect_file_name(self):
        ''' Confirm the executable file if there is multiple files that are runnable in current folder
        '''
        cdef:
            object existed_templates = {}
            object acceptable_file_ext = {}
            string alias
            string res
            int opt = 0

        with open(self.kt_config) as f:
            existed_templates = json.load(f)
        
        for k, v in existed_templates.items():
            acceptable_file_ext[map_template_to_plang[k].extension] = map_template_to_plang[k]

        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        runnable_files = []
        for f in files:
            parts = f.split('.')
            if len(parts) <= 1:
                continue
            if  parts[1] in acceptable_file_ext:
                runnable_files.append((parts[0], f, parts[1]))
        
        if len(runnable_files) == 0:
            raise RuntimeError('Not executable code file detected')
        
        if len(runnable_files) > 1:
            print(color_cyan(b'Choose a file to run'))
            for i in range(len(runnable_files)):
                print(f'  {i}: {runnable_files[i][1]}')
            res = input()
            opt = int(res)
            assert 0 <= opt < len(runnable_files), 'Invalid option chosen'

        
        self.file_name = runnable_files[opt][0]
        alias = acceptable_file_ext[runnable_files[opt][2]].alias
        self.lang = acceptable_file_ext[runnable_files[opt][2]].full_name
        self.pre_script = existed_templates.get(alias, {}).get('pre_script').replace('$%file%$', self.file_name)
        self.script = existed_templates.get(alias, {}).get('script').replace('$%file%$', self.file_name)
        self.post_script = existed_templates.get(alias, {}).get('post_script').replace('$%file%$', self.file_name)


    cdef _act(self):
        ''' Run the executable file against sample input and output files present in the folder
        The sample files will only be recognized if the conditions hold:
        - Naming style should be in{idx}.txt and ans{txt}.txt
        - for in{idx}.txt, there must exist a ans{idx}.txt with the same `idx`
        '''
        cdef:
            int idx
            float start_time
            float taken
            vector[string] actual
            vector[string] expected
            vector[string] diff
            vector[string] ith_line_exp
            vector[string] ith_line_actual
            string current_diff
            bool_t is_ac
            string raw_output
            string stderr_data
            string lhs
            string rhs
            string temp
            float mem_used
            long rusage_denom = 1 << 20
            object p

        self.detect_file_name()
        input_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.startswith('in')]
        output_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.startswith('ans')]
        usable_samples = []
        
        # Get sample files that match the condition
        Sample = namedtuple('Sample', 
            ['index', 'input_file', 'output_file']
        )
        pattern = re.compile(r"\d+")
        for input_file in input_files:
            idx = int(pattern.search(input_file).group(0))
            for output_file in output_files:
                if idx == int(pattern.search(output_file).group(0)):
                    usable_samples.append(Sample(idx, input_file, output_file))
                    break
        # run test from ascending number of file index
        usable_samples = sorted(usable_samples, key=lambda x: x.index)
        # run test
        print(f'Problem ID : {color_cyan(self.get_problem_id())}')
        print(f'Lanuage    : {self.lang}')
        if self.pre_script.size() > 0:
            subprocess.check_call(shlex.split(self.pre_script))

        for sample in usable_samples:
            is_ac = True
            actual.clear()
            expected.clear()
            diff.clear()
            try:
                with open(sample.output_file, 'r') as f:
                    expected = [l.strip(" \n") for l in f.readlines()]
                with open(sample.input_file, 'rb') as f:
                    raw_input = f.read()

                p = Popen([self.script, '-'], stdin=PIPE, stdout=PIPE, shell=False, 
                    preexec_fn=os.setsid)
                test_subprocesses.append(p)
                proc = psutil.Process(p.pid)
                mem_used = proc.memory_info().rss / rusage_denom
                start_time = time.perf_counter()
                raw_output = p.communicate(raw_input)[0]
                p.wait()
                taken = time.perf_counter()  - start_time
                
                actual = [z.strip(" \n") for z in raw_output.split('\n')]
                make_list_equal(actual, expected)
                diff.clear()

                for i in range(len(expected)):
                    ''' Compare the values line by line
                    For each line, compare the values from left to right. 
                    '''
                    ith_line_exp = [z for z in expected[i].split(' ')]
                    ith_line_actual = [z for z in actual[i].split(' ')]

                    make_list_equal(ith_line_exp, ith_line_actual)
                    current_diff.clear()
                    for j in range(len(ith_line_exp)):
                        lhs = ith_line_exp[j]
                        rhs = ith_line_actual[j]
                        is_ac &= compare_entity(rhs,lhs, current_diff)

                    diff.push_back(current_diff)
                if is_ac:
                    print(color_green(f'Test Case #{sample.index}: {"Accepted".ljust(13, " ")} ... {taken:.3f} s   {mem_used:.2f} Mb'))
                else:
                    print(color_red(f'Test Case #{sample.index}: {"Wrong Answer".ljust(13, " ")} ... {taken:.3f} s   {mem_used:.2f} Mb'))
                    print(color_cyan(b'--- Input ---'))
                    print(raw_input.decode('utf-8'))
                    print(color_cyan(b'--- Diff ---'))
                    for i in range(diff.size()):
                        print(diff[i])

            except Exception as e:
                print(color_red(f'Test case #{sample.index}: Runtime Error {e}'))
        if self.post_script.size() > 0:
            subprocess.check_call(shlex.split(self.post_script))


cdef class Submit(Action):
    '''Handle kt submit action to push the file to kattis website'''
    cdef:
        string ac_icon
        string rj_icon
        string sk_icon

        string file_name
        string lang
        string submission_id
        string problem_id

    def __cinit__(self):
        self.ac_icon = b':heavy_check_mark:'
        self.rj_icon = b':heavy_multiplication_x:'
        self.sk_icon = b':white_medium_square:'
        

    cdef bool_t is_finished(self, object output_lines, object result, string& status, string run_time): 
        ''' Judge whether the result and status obtained from kattis submission
        page has indicated whether the solution judgement has been done
        Args:
        - output_lines console object to print multiple lines inline
        - result: List of object corresponding to the HTML component of test case on kattis submission
        page
        - status: Status obtained from kattis submission page
        - run_time: Time taken obtained from kattis submissione page
        '''   
        cdef:
            int tot_res = len(result)
            int ac_ct = 0
            bool_t is_ac = True
            bool_t rejected = False
            bool_t finished = False
            string _status = status

        for res in result:
            _class = res.get('class', None)
            if _class:
                if _class[0] == 'accepted':
                    ac_ct += 1
                else: # rejected
                    rejected = True
                    is_ac = False
                    break
        res = [self.ac_icon] * ac_ct

        if rejected:
            res.append(self.rj_icon)
        while len(res) < tot_res:
            res.append(self.sk_icon)

        if rejected:
            finished = True
        else:
            finished = ac_ct == tot_res

        if status == b'Compiling':
            finished = False
        elif status == b'Compile Error':
            _status = color_red(status)
        elif not finished:
            _status = color_cyan(status)
        else:
            if status == b'Running': # status text not updated, lets try again
                finished = False
            elif is_ac:
                _status = color_green(status)
            else:
                _status = color_red(status)

        output_lines['current time      '] = f"{time.strftime('%02l:%M%p %Z on %b %d, %Y')}"
        output_lines['language          '] = f'{self.lang}' 
        output_lines['problem id        '] = self.problem_id
        output_lines['running time      '] = f'{run_time}' 
        output_lines['submission id     '] = self.submission_id
        output_lines['submission result '] = f'{_status}'
        output_lines['test cases        '] = f"{emoji.emojize(' '.join(res))}"
        return finished
        


    cdef _render_result(self, string submission_url_ret):
        ''' Continuously polling for result from `submission_url_ret`
        Args:
        - submission_url_ret: url for the submission to be checked
        '''
        cdef:
            int time_out = 20
            float cur_time = 0
            string status_ret
            string runtime_ret
            bool_t done  = False


        with output(output_type='dict') as output_lines:
            while cur_time < time_out and not done:
                try:
                    self.login()
                    page = requests.get(submission_url_ret, cookies=self.cookies, headers=_HEADERS)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    submission_data = soup.find('div', class_='testcases')
                    submission_ret = submission_data.find_all('span')
                    status_ret = soup.find('td', class_='status middle').find('span').text
                    runtime_ret = soup.find('td', class_='runtime middle').text
                    done = self.is_finished(output_lines, submission_ret, status_ret, runtime_ret)
                except Exception as e:
                    print(color_red(f'Internal error: {e}'))

                time.sleep(0.4)
                cur_time += 0.4


    cdef detect_file_name(self):
        ''' Detect executable file to submit for kattis judge if there are multiple files
        that are executable based on user ktconfig file
        '''
        cdef:
            object acceptable_file_ext = {}
            string alias
            int opt = 0
            int res_int
            string res

        for k, v in map_template_to_plang.items():
            acceptable_file_ext[map_template_to_plang[k].extension] = map_template_to_plang[k]
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        runnable_files = []
        RunnableFile = namedtuple('RunnableFile',
            ['file_name', 'full_name', 'ext']
        )
        for f in files:
            parts = f.split('.')
            if len(parts) <= 1:
                continue
            if parts[1] in acceptable_file_ext:
                runnable_files.append(RunnableFile(parts[0], f, parts[1]))

        if len(runnable_files) == 0:
            raise RuntimeError('Not executable code file detected')

        if len(runnable_files) > 1:
            print(color_cyan(b'Choose a file:'))
            for i in range(len(runnable_files)):
                print(f'  {i}: {runnable_files[i].full_name}')
            res = input()
            opt = int(res)
            assert 0 <= opt < len(runnable_files), 'Invalid option chosen'
        self.problem_id = runnable_files[opt].file_name
        self.file_name = os.path.abspath(runnable_files[opt].full_name) 
        if runnable_files[opt].ext == 'py':
            res = input('Which python version you want to submit, 2 or 3?\n')
            res_int = int(res)
            assert 2 <= res_int <= 3, "Invalid option"
            self.lang = f'Python {res_int}'
        else:
            self.lang = acceptable_file_ext[runnable_files[opt].ext].full_name
            

    cdef _act(self):
        '''Submit the code file for kattis judge'''
        cdef:
            string err
            string submissions_url
            string submission_url_ret
            string submit_response
            string problem_id = self.get_problem_id()

        self.detect_file_name()
        data = {'submit': 'true',
            'submit_ctr': 2,
            'language': self.lang,
            'mainclass': '',
            'problem': problem_id,
            'tag': '',
            'script': 'true'}
        files = []
        with open(self.file_name) as sub_file:
            files.append(('sub_file[]',
                              (os.path.basename(self.file_name),
                               sub_file.read(),
                               'application/octet-stream')))
        submit_url = self.get_url(b'submissionurl', b'submit')
        self.login()
        ret = requests.post(submit_url, data=data, files=files, 
            cookies=self.cookies, headers=_HEADERS)
        if ret.status_code != 200:
            if ret.status_code == 403:
                err = b'Access denied (403)'
            elif ret.status_code == 404:
                err = b'Incorrect submit URL (404)'
            else:
                err = f'Status code: {ret.status_code}'
            raise RuntimeError(f'Submission failed: {err}')
        submissions_url  = self.get_url(b'submissionsurl', b'submissions')
        submit_response = ret.content.decode('utf-8').replace('<br />', '\n')
        self.submission_id = re.search(r'Submission ID: (\d+)', submit_response).group(1)
        print(color_green(b'Submission successful'))
        submission_url_ret  = f'{submissions_url}/{self.submission_id}' 
        self._render_result(submission_url_ret)


cdef class Config(Action):
    cdef add_template(self):
        cdef:
            string question = b'Which template would you like to add:\n'
            string temp
            object selectable_lang = {}
            int idx = 1
            object existed_templates = {}
            string res
            int ret
            object options = {}

        print(color_green(b'Adapted from xalanq\'s cf tool'))
        print('''
Template will run 3 scripts in sequence when you run "kt test":
    - before_script   (execute once)
    - script          (execute the number of samples times)
    - after_script    (execute once)
You could set "before_script" or "after_script" to empty string, meaning not executing.
You have to run your program in "script" with standard input/output (no need to redirect).

You can insert some placeholders in your scripts. When execute a script,
cf will replace all placeholders by following rules:

$%path%$   Path to source file (Excluding $%full%$, e.g. "/home/user/")
$%full%$   Full name of source file (e.g. "a.cpp")
$%file%$   Name of source file (Excluding suffix, e.g. "a")
$%rand%$   Random string with 8 character (including "a-z" "0-9")
        ''')
        

        with open(self.kt_config) as f:
            existed_templates = json.load(f)

        for template_type, lang in map_template_to_plang.items():
            if template_type not in existed_templates:
                temp = f'{idx} ({lang.extension}): {lang.full_name}\n'
                question.append(temp)
                selectable_lang[idx] = (template_type, lang)
                idx += 1

        res = input(question)
        ret = int(res)
        assert 1 <= ret < idx, 'Invalid input'
        
        selected_lang = selectable_lang[ret][1]
        options['path'] = ask_with_default(b'Template path', f'~/template.{selected_lang.extension}')
        options['pre_script'] = ask_with_default(b'Pre-script', selected_lang.pre_script)
        options['script'] = ask_with_default(b'Script', selected_lang.script)
        options['post_script'] = ask_with_default(b'Post-script', selected_lang.post_script)
        options['default'] = False if existed_templates else True

        existed_templates[selected_lang.alias] = options
        with open(self.kt_config, 'w') as kt_config:
            json.dump(existed_templates, kt_config, indent=2)
        print(color_green(b'Yosh, your configuration has been saved'))


    cdef remove_template(self):
        ''' Remove a template from ktconfig file'''
        cdef:
            object existed_templates = {}
            str res
            bool_t move_default

        with open(self.kt_config) as f:
            existed_templates = json.load(f)

        print(f'Which template would you like to {color_red(b"delete")} ? For eg cpp, cc, ...')
        for k, v in existed_templates.items():
            print(k)
        res = input()

        assert res in existed_templates, f'Invalid template chosen. Template {res} is not in ur config file'

        move_default = existed_templates[res]['default']
        existed_templates.pop(res, None)
        if existed_templates and move_default: # move default to the first key of template
            existed_templates[next(iter(existed_templates))] = True
        with open(self.kt_config, 'w') as kt_config:
            json.dump(existed_templates, kt_config, indent=2)

    cdef update_default(self):
        cdef:
            object existed_templates = {}
            str res
            string default_key = b''

        with open(self.kt_config) as f:
            existed_templates = json.load(f)
        print(f'Which template would you like to gen as {color_cyan(b"default")} ? For eg cpp, cc, ...')
        
        for k, v in existed_templates.items():
            print(f'{k} {color_green(b"(default)") if v["default"] else ""}')
            if v["default"]:
                default_key = k
        res  = input()

        assert res in existed_templates, f'Invalid template chosen. Template {res} is not in ur config file'
        existed_templates[default_key]["default"] = False
        existed_templates[res]["default"] = True
        with open(self.kt_config, 'w') as kt_config:
            json.dump(existed_templates, kt_config, indent=2)
        print(color_green(b'Yosh, your configuration has been saved'))

    cdef _act(self):
        cdef:
            string question = color_cyan(b'Select an option:\n')
            string res
            int opt
        question.append(b"""1: Add a template
2: Remove a template
3: Select a default template
""")
        res = input(question)
        opt = int(res)
        if opt == 1:
            self.add_template()
        elif opt == 2:
            self.remove_template()
        elif opt == 3:
            self.update_default()
        else:
            raise ValueError('Invalid option')

cdef class Open(Action):
    cdef _act(self):
        webbrowser.open(self.get_problem_url())

cdef class Version(Action):
    cdef _act(self):
        print(f'Current version: {color_cyan(_VERSION)}')

cdef class Update(Action):
    cdef _act(self):
        cdef:
            object pypi_info 
            vector[string] releases
            string current_latest_version

        pypi_info = requests.get(_PYPI_PACKAGE_INFO)
        releases = list(pypi_info.json()['releases'])
        if len(releases) == 0:
            print(color_red(b'Hmm seems like there is currently no pypi releases :-?'))
            return
        current_latest_version = releases.back()
        if current_latest_version != _VERSION:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "--no-cache-dir", f"kttool=={current_latest_version}"])
            print(f'Installed version {color_green(current_latest_version)} successfully!')
        else:
            print(f'You already have the {color_green(b"latest")} version!')


cdef object map_key_to_class = {
    'gen': Gen,
    'test': Test,
    'submit': Submit,
    'config': Config,
    'open': Open,
    'version': Version,
    'update': Update
} 

cpdef Action arg_parse(list args):
    ''' Generate an appropriate command class based on user command stirng '''
    if len(args) == 0:
        raise ValueError(f'No command provided to kt')
    if args[0] not in map_key_to_class:
        raise ValueError(f'First argument should be one of {list(map_key_to_class.keys())}')
    return map_key_to_class[args[0]](*args[1:])


cpdef exit_gracefully(signum, frame):
    original_sigint = signal.getsignal(signal.SIGINT)
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    for sp in test_subprocesses:
        try:
            sp.kill()
        except:
            pass
    print(color_green(b'Great is the art of beginning, but greater is the art of ending.'))
    sys.exit(1)
    

    