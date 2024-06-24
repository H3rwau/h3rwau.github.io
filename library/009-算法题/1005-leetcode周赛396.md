## 有效单词

```c++
class Solution {
public:
    unordered_set<char> uset{'a','e','i','o','u'};
    bool isValid(string word){
        bool f1=false,f2=false;
        if(word.size()<3)
            return false;
        for(auto &c:word)
        {
            if(isalpha(c)!=0){
                if(uset.count(tolower(c))>0)
                    f1 = true;
                else
                    f2 = true;
             }else if(isdigit(c)==0){
                return false;
            }   
        }
        return f1&&f2;
    }
};
```

## K 周期字符串需要的最少操作次数

```c++
class Solution {
public:
    int minimumOperationsToMakeKPeriodic(string word, int k) {
        //先找到对应的模板串
        unordered_map<string,int> twmap;
        for(int i=0;i<word.size();i+=k){
            string tw(word.begin()+i,word.begin()+i+k);
            twmap[tw]++;
        }
        int freq=0;
        for(auto &p:twmap){
            if(p.second>freq)
                freq=p.second;
        }
        return (word.size()/k)-freq;
    }
};
```

## 同位字符串连接的最小长度

```c++
class Solution {
public:
    int minAnagramLength(string s) {
        int res=s.size();
        for(int i=0;i<s.size()-1;i++){
            //s[0:i]
            int len = i+1;
            if(s.size()%len!=0)
                continue;
            //int aset =0;
            vector<int > frq(26,0);
            int j=0;
            for(;j<=i;j++){
                int c = s[j]-'a';
                //aset |=(1<<c);
                ++frq[c];
            }

            int flag = 0;
            for(int k =i+1;k<s.size()&&!flag;k+=len){
                //bset =0;
                vector<int > tfrq(26,0);
                for(int l =k;l<k+len;l++){
                    int c = s[l]-'a';
                    ++tfrq[c];
                    //bset |=(1<<c);
                }
                if(tfrq!=frq)
                    flag = 1;
            }
            if(0==flag)
                res=min(res,len);          
        }
        return res;
        
    }
};
```



