#include<bits/stdc++.h>
using namespace std;
int main(){
    int t;
    cin>>t;
    int m=1;
    while(m<=t){
        
        int n,k;
        cin>>n>>k;
        vector<int> v(n);
        map<int,int> mp;
        for(int i=0;i<n;i++){
            cin>>v[i];
            mp[v[i]]++;
        }
        cout<<"Case #"<<m<<": ";
        bool found=false;
        for(auto x: mp){
            if(x.second>2){
                found=true;
                break;
            }
        }
        if(found){
            cout<<"NO"<<endl;
        }
        else if(k>=n-n/2){
            cout<<"YES"<<endl;
        }
        else {
            cout<<"NO"<<endl;
        }
        m++;
    }
    return 0;
}