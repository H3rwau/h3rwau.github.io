## [100286. 构造相同颜色的正方形](https://leetcode.cn/problems/make-a-square-with-the-same-color/)

```c++
class Solution {
public:
    bool canMakeSquare(vector<vector<char>>& grid) {
        auto check = [&](int i, int j) {
            int cnt[2]{};
            cnt[grid[i][j] & 1]++;
            cnt[grid[i][j + 1] & 1]++;
            cnt[grid[i + 1][j] & 1]++;
            cnt[grid[i + 1][j + 1] & 1]++;
            return cnt[0] >= 3 || cnt[1] >= 3;
        };
        return check(0, 0) || check(0, 1) || check(1, 0) || check(1, 1);
    }
};
```

## [100278. 直角三角形](https://leetcode.cn/problems/right-triangles/)

```c++
class Solution {
public:
    long long numberOfRightTriangles(vector<vector<int>>& grid) {
        int n = grid[0].size();
        vector<int> col_sum(n, -1); // 提前减一
        for (int j = 0; j < n; j++) {
            for (auto& row : grid) {
                col_sum[j] += row[j];
            }
        }

        long long ans = 0;
        for (auto& row : grid) {
            int row_sum = accumulate(row.begin(), row.end(), 0) - 1; // 提前减一
            for (int j = 0; j < row.size(); j++) {
                if (row[j] == 1) {
                    ans += row_sum * col_sum[j];
                }
            }
        }
        return ans;
    }
};
```

## [100293. 找出所有稳定的二进制数组 II](https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-ii/)

初步思路：

dfs(i,j,k) 表示用i个0，j个1构造**稳定二进制数组**的**方案数**，其中第i+k个位置要填k（0 or 1）

k=0:  **dfs(i,j,0) = dfs(i-1,j,1)+dfs(i-1,j,0)-dfs(i-limit-1,j,1)**

由于原先是合法方案，假设最后一位加了0后变成了非法方案，那么需要减掉生成非法方案的组合个数，也就是dfs(i-limit-1,j,1),末尾是limit+1个零，已经是非法了，那么前面有多少个组合呢。答案 是这个dfs(i-limit-1,j,1)

```c++
class Solution {
public:
    int numberOfStableArrays(int zero, int one, int limit) {
        const int MOD = 1e9+7;
        //用i个0，j个1构造稳定二进制数组的方案数，其中第i+k个位置要填k（0 or 1）
        vector<vector<array<int, 2>>> f(zero + 1, vector<array<int, 2>>(one + 1));
        for (int i = 1; i <= min(limit, zero); i++) {
            f[i][0][0] = 1;
        }
        for (int j = 1; j <= min(limit, one); j++) {
            f[0][j][1] = 1;
        }
        for (int i = 1; i <= zero; i++) {
            for (int j = 1; j <= one; j++) {
                // + MOD 保证答案非负
                f[i][j][0] = ((long long) f[i - 1][j][0] + f[i - 1][j][1] + (i > limit ? MOD - f[i - limit - 1][j][1] : 0)) % MOD;
                f[i][j][1] = ((long long) f[i][j - 1][0] + f[i][j - 1][1] + (j > limit ? MOD - f[i][j - limit - 1][0] : 0)) % MOD;
            }
        }
        return (f[zero][one][0] + f[zero][one][1]) % MOD;
    }
};

```

