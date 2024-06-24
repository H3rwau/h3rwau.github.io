## [3114. 替换字符可以得到的最晚时间](https://leetcode.cn/problems/latest-time-you-can-obtain-after-replacing-characters/)

直接判断：

```c++
class Solution {
public:
    string findLatestTime(string s) {
        if (s[0] == '?') {
            s[0] = s[1] == '?' || s[1] <= '1' ? '1' : '0';
        }
        if (s[1] == '?') {
            s[1] = s[0] == '1' ? '1' : '9';
        }
        if (s[3] == '?') {
            s[3] = '5';
        }
        if (s[4] == '?') {
            s[4] = '9';
        }
        return s;
    }
```

枚举：

```c++
class Solution {
public:
    string findLatestTime(string s) {
        for (int h = 11; ; h--) {
            if (s[0] != '?' && s[0] - '0' != h / 10 || s[1] != '?' && s[1] - '0' != h % 10) {
                continue;
            }
            for (int m = 59; m >= 0; m--) {
                if (s[3] != '?' && s[3] - '0' != m / 10 || s[4] != '?' && s[4] - '0' != m % 10) {
                    continue;
                }
                char ans[6];
                sprintf(ans, "%02d:%02d", h, m);
                return string(ans);
            }
        }
    }
};
```



## [3115. 质数的最大距离](https://leetcode.cn/problems/maximum-prime-difference/)

```c++
class Solution {
    bool is_prime(int n) {
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                return false;
            }
        }
        return n >= 2;
    }

public:
    int maximumPrimeDifference(vector<int>& nums) {
        int i = 0;
        while (!is_prime(nums[i])) {
            i++;
        }
        int j = nums.size() - 1;
        while (!is_prime(nums[j])) {
            j--;
        }
        return j - i;
    }
};
```

