#include<bits/stdc++.h>
using namespace std;
int main()
{ long long int t;
  cin>>t;
  while(t--)
  {
  long long int a,b;
  cin>>a>>b;
  long long int bitA = __builtin_popcount (a), bitB = __builtin_popcount (b);
  long long int bitb = __builtin_popcount (b-1), bita = __builtin_popcount (a-1);
  long long int res = 0,steps=0,i=-1,p=0;
  //cout<<bitA<<" "<<bitB<<endl;
  while(res==0 && b!=0)
  {
      p = pow(2,++i);
      res = b & p;
  }
  if(a==b) steps=0;
  else if(b%2!=0 && b!=0 && b!=1)
  {
      if(bitA==bitB) steps = 2;
      else if(bitA<bitB) steps = bitB-bitA;
      else if(bitA>bitB) steps=2;
  }
  else if(b%2==0 && b!=0 && b!=1)
  {
      //cout<<"Hi there!!"<<endl;
      if(bitA==bitB) steps = i;
      else if(bitA<bitB) steps = bitB - bitA + i;
      else if(bitA>bitB) {
        if((bitA-bitB)>=i) steps=2;
        else steps = i-(bitA-bitB);
      }
  }
  else if((b==0 && a!=0)||(b==1 && a!=0))
    steps = -1;
  cout<<steps<<endl;
    }
 
  return 0;
 }
 