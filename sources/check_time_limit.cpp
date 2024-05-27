#include <iostream>
#include <vector>
#include <chrono>
#include <unistd.h>
#include <sys/resource.h>
#include <sys/wait.h>

using namespace std;
using namespace chrono;

void sum_positive_numbers(const vector<int>& arr) {
    while(true) {}
    int total = 0;
    for (int num : arr) {
        if (num > 0) {
            total += num;
        }
    }
}

int main() {
    int n = 3;
    vector<int> arr = {1, 3 , 1};
 

    pid_t child_pid = fork();
    if (child_pid == 0) {
        // Child process
        struct rlimit rl;
        getrlimit(RLIMIT_CPU, &rl);
        rl.rlim_cur = 1;  // Устанавливаем ограничение времени на 1 секунду
        setrlimit(RLIMIT_CPU, &rl);

        sum_positive_numbers(arr);
        exit(0);
    } else {
        // Parent process
        int status;
        auto start_time = high_resolution_clock::now();
        waitpid(child_pid, &status, 0);
        auto end_time = high_resolution_clock::now();

        auto duration = duration_cast<milliseconds>(end_time - start_time);
        if (WIFSIGNALED(status)) {
            cout << "Time limit exceeded" << endl;
        } else {
            cout << "Execution time: " << duration.count() << " milliseconds" << endl;
        }
    }

    return 0;
}