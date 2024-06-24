初步思路：

由于只移除两个元素，可以枚举nums1中保留的最小元素是nums1[0],nums1[1]还是nums1[2]

```c++
class Solution {
public:
    int minimumAddedInteger(vector<int>& nums1, vector<int>& nums2) {
        ranges::sort(nums1);
        ranges::sort(nums2);
        // 枚举保留 nums1[2] 或者 nums1[1] 或者 nums1[0]
        // 倒着枚举是因为 nums1[i] 越大答案越小，第一个满足的就是答案
        for (int i = 2; i; i--) {
            int diff = nums2[0] - nums1[i];
            // 在 {nums1[i] + diff} 中找子序列 nums2
            int j = 0;
            for (int k = i; k < nums1.size(); k++) {
                if (j < nums2.size() && nums2[j] == nums1[k] + diff && ++j == nums2.size()) {                
                    // nums2 是 {nums1[i] + diff} 的子序列
                    return diff;
                }
            }
        }
        // 题目保证答案一定存在
        return nums2[0] - nums1[0];
    }
};
```

## [100282. 数组最后一个元素的最小值](https://leetcode.cn/problems/minimum-array-end/)

初步思路：数组里最小的数就是x，由于与操作不会使得数字变大，那么我们只需要找到第n-1小的数字其实也就是从0开始的自然增长的第n-1小的数字。将其的比特位移到x上也就是找到了答案。

```c++
class Solution {
public:
    long long minEnd(int n, int x) {
        n--; // 先把 n 减一，这样下面讨论的 n 就是原来的 n-1
        long long ans = x;
        int i = 0, j = 0;
        while (n >> j) {
            // x 的第 i 个比特值是 0，即「空位」
            if ((ans >> i & 1) == 0) {
                // 空位填入 n 的第 j 个比特值
                int bit =  (long long) (n >> j & 1);
                ans |= bit << i;
                j++;
            }
            i++;
        }
        return ans;
    }
};

```

优化:把x取反，用 lowbit 枚举其中的 1，就是要填的空位。

```c++
class Solution {
public:
    long long minEnd(int n, int x) {
        n--;
        long long ans = x;
        int j = 0;
        for (long long t = ~x, lb; n >> j; t ^= lb) {
            lb = t & -t;
            ans |= (long long) (n >> j++ & 1) * lb;
        }
        return ans;
    }
};

```

