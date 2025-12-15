import time
import httpx

BASE = "http://127.0.0.1:8000"

def wait_for_server(timeout=20):
    for i in range(timeout):
        try:
            r = httpx.get(BASE)
            if r.status_code == 200:
                print('Server is up')
                return True
        except Exception:
            pass
        time.sleep(1)
    raise SystemExit('Server did not become ready')


def run_tests():
    wait_for_server()
    client = httpx.Client(base_url=BASE)

    # Create student
    r = client.post('/students/', json={'name': 'alice'})
    print('POST /students/ ->', r.status_code, r.text)

    # Create teacher
    r = client.post('/teachers/', json={'name': 'mrsmith'})
    print('POST /teachers/ ->', r.status_code, r.text)

    # Submit assignment with file
    with open('test_upload.txt', 'rb') as f:
        files = {'file': ('test_upload.txt', f)}
        data = {'student_name': 'alice', 'subject': 'Math', 'description': 'Homework 1'}
        r = client.post('/assignments/', data=data, files=files)
    print('POST /assignments/ ->', r.status_code, r.text)

    # List assignments
    r = client.get('/assignments/')
    print('GET /assignments/ ->', r.status_code, r.text)

    # List assignments for student
    r = client.get('/students/alice/assignments/')
    print('GET /students/alice/assignments/ ->', r.status_code, r.text)

    # Add a comment
    assignments = r.json()
    if assignments:
        assignment_id = assignments[0]['id']
        r = client.post(f'/assignments/{assignment_id}/comment', data={'teacher_name': 'mrsmith', 'comment': 'Good job'})
        print(f'POST /assignments/{assignment_id}/comment ->', r.status_code, r.text)
    else:
        print('No assignments found to comment on')

    print('All tests finished')

if __name__ == '__main__':
    run_tests()
