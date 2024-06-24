## [3105. 最长的严格递增或递减子数组](https://leetcode.cn/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/)

**解题思路：** 出现拐点即可计算长度，利用bool inc = a[i+1]>a[i];保证当前序列是计算同一种递增或者递减。

```c++
class Solution {
public:
    int longestMonotonicSubarray(vector<int>& a) {
        int ans =1;
        int len = a.size();
        //分组循环
        int i=0;
        while(i<len-1){
            if(a[i+1]==a[i]){
                i++;
                continue;
            }
            int i0=i;
            bool inc = a[i+1]>a[i];
            i+=2;
            while(i<len&&a[i]!=a[i-1]&&(a[i]>a[i-1])==inc)
                i++;
            ans=max(ans,i-i0);
            i--;
        }
        return ans;
    }
};
```

## [3106. 满足距离约束且字典序最小的字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-operations-with-constraint/)

**解题思路：**求出字符和a的最小距离int dis = min(s[i] - 'a', 'z' - s[i] + 1);然后如果最小距离小于k，证明只能变化k个距离，那么变化完后直接break，如果最小距离大于大于k,那么直接将该字符变a，并且k-=dis，遍历下一个字符。

```c++
class Solution {
public:
    string getSmallestString(string s, int k) {
        for (int i = 0; i < s.size(); i++) {
            int dis = min(s[i] - 'a', 'z' - s[i] + 1);
            if (dis > k) {
                s[i] -= k;
                break;
            }
            k-=dis;
            s[i]='a';
        }
        return s;
    }
};
```



## [3107. 使数组中位数等于 K 的最少操作数](https://leetcode.cn/problems/minimum-operations-to-make-median-of-array-equal-to-k/)

**解题思路：**对数组排序，如果数组的中间的数字小于k，那么只需要保证中间数字到数组末尾的数字都大于等于k就可以了，如果数组的中间的数字大于k，那么只需要保证中间数字到数组开端的数字都小于等于k就可以了。



```c++
class Solution {
public:
    long long minOperationsToMakeMedianK(vector<int>& nums, int k) {
        sort(nums.begin(),nums.end());
        int mid = nums.size()/2;
        long long  ans=0;
        if(nums[mid]>k){
            for(int i=mid;i>=0;i--){
                if(nums[i]<=k)
                    break;
                ans += (nums[i]-k);
            }
        }else {
            for(int i=mid;i<nums.size();i++){
                if(nums[i]>=k)
                    break;
                ans += (k-nums[i]);
            }
        }
        return ans;
    }
};
```

**扩展：**简单的理解 **nth_element()** 函数的功能，当采用默认的升序排序规则（std::less<T>）时，该函数可以从某个序列中找到第 n 小的元素 K，并将 K 移动到序列中第 n 的位置处。不仅如此，整个序列经过 nth_element() 函数处理后，所有位于 K 之前的元素都比 K 小，所有位于 K 之后的元素都比 K 大。

```cpp
class Solution {
public:
    long long minOperationsToMakeMedianK(vector<int> &nums, int k) {
        int m = nums.size() / 2;
        ranges::nth_element(nums, nums.begin() + m);
        long long ans = 0;
        if (nums[m] > k) {
            for (int i = 0; i <= m; i++) {
                ans += max(nums[i] - k, 0);
            }
        } else {
            for (int i = m; i < nums.size(); i++) {
                ans += max(k - nums[i], 0);
            }
        }
        return ans;
    }
};
```

## [3108. 带权图里旅途的最小代价](https://leetcode.cn/problems/minimum-cost-walk-in-weighted-graph/)

**dfs方法：**

```c++
class Solution {
public:
vector<vector<pair<int,int>>> g;
vector<int> cc_and,ids;

    int dfs(int x){
        ids[x]=cc_and.size();
        int and_=-1;
        for(auto &[y,w]:g[x]){
            and_ &= w;
            if(ids[y]<0)
                and_&=dfs(y);
        }
        return and_;
    }
    vector<int> minimumCost(int n, vector<vector<int>>& edges, vector<vector<int>>& query) {
        g.resize(n);
        for(auto &e:edges){
            int x=e[0],y=e[1],w=e[2];
            g[x].emplace_back(y,w);
            g[y].emplace_back(x,w);
        }

        ids.resize(n,-1);
        for(int i=0;i<n;i++){
            if(ids[i]<0)
                cc_and.push_back(dfs(i));
        }

        vector<int> ans;
        ans.reserve(query.size());
        for(auto &q:query){
            int s=q[0],t=q[1];
            ans.push_back(ids[s]!=ids[t]?-1:cc_and[ids[s]]);
        }
        return ans;
    }
};
```

**并查集**

```c++
class Solution {
public:
vector<int> fa,and_;
int find(int x){
    return fa[x]==x?x:fa[x]=find(fa[x]);
}
    vector<int> minimumCost(int n, vector<vector<int>>& edges, vector<vector<int>>& query) {
        fa.resize(n);
        iota(fa.begin(),fa.end(),0);
        and_.resize(n,-1);
        for(auto &e:edges){
            int x=find(e[0]);
            int y=find(e[1]);
            and_[y]&=e[2];
            if(x!=y){
                and_[y]&=and_[x];
                fa[x]=y;
            }
        }

        vector<int> ans;
        ans.reserve(query.size());
        for(auto &q:query){
            int s=q[0],t=q[1];
            ans.push_back(find(s)!=find(t)?-1:and_[find(s)]);
        }
        return ans;
    }
};
```

