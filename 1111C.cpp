/* 
    Author - linpaws07 
*/
#include <bits/stdc++.h>
using namespace std;
using namespace std::chrono;
#define mod 1000000007
#define mp make_pair
#define pb push_back
#define inf (int)1e9
#define f first
#define s second
#define eps 1e-9
#define PI 3.1415926535897932384626433832795
#define scd(t) scanf("%d",&t)
#define sclld(t) scanf("%lld",&t)
#define scc(t) scanf("%c",&t)
#define scs(t) scanf("%s",t)
#define scf(t) scanf("%f",&t)
#define sclf(t) scanf("%lf",&t)
#define memst(a, b) memset(a, (b), sizeof(a))
typedef pair<int, int> pii;
typedef vector<int> vi;
typedef vector<string> vs;
typedef vector<pii> vii;
typedef vector<vi> vvi;
typedef map<int,int> mpii;
typedef set<int> seti;
typedef multiset<int> mseti;
typedef long int int32;
typedef unsigned long int uint32;
typedef long long int int64;
typedef unsigned long long int uint64;
#define FAST ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);
#define DEBUG(x) cout << '>' << #x << ':' << x << endl;
#define rp(i,n) for(int i=0;i<(n);i++)
#define fr(i,a,b) for(int i=(a);i<(b);i++)
#define fre(i,a,b) for(int i=(a);i<=(b);i++)
#define frd(i,a,b) for(int i=(a);i>=(b);i--)
inline bool eq(double a, double b) { return fabs(a-b) < 1e-9; }
inline int two(int n) { return 1 << n; }
inline int test(int n, int b) { return (n>>b)&1; }
inline void set_bit(int & n, int b) { n |= two(b); }
inline void unset_bit(int & n, int b) { n &= ~two(b); }
inline int last_bit(int n) { return n & (-n); }
inline int ones(int n) { int res = 0; while(n && ++res) n-=n&(-n); return res; }
auto start = high_resolution_clock::now();
inline void measure();

int64 n, k, A, B;
int64 p[100002];
int64 solve(int64 l, int64 r){
    if(r == 0){
        int64 lf = l;
        int64 ct1 = lower_bound(p, p + k, lf) - p;
        int64 ct2 = upper_bound(p, p + k, lf) - p;
        int64 na = ct2 - ct1;
        if(na < 0)   na = 0;
        int64 ans = ((na == 0) ?  A : B * na * 1);
        return ans;
    }
    int64 lf = l;
    int64 rg = l + (1<<r) - 1;
    int64 ct1 = lower_bound(p, p + k, lf) - p;
    int64 ct2 = upper_bound(p, p + k, rg) - p;
    int64 na = ct2 - ct1;
    if(na < 0)   na = 0;
    int64 ans;
    if(na == 0) ans = A;
    else ans = min((solve(l, r - 1) + solve(l + (1 << (r - 1)), r - 1)), (na == 0) ?  A : B * na * (rg - lf + 1));
    return ans;
}
int main(){
    FAST
    //Do awesome things here
    cin >> n >> k >> A >> B;
    rp(i, k){
        cin >> p[i];
    }
    sort(p, p + k);
    int64 ans = solve(1, n);
    cout << ans << endl;
    return 0;
}


inline void measure(){
    auto stop = high_resolution_clock::now(); 
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << duration.count() << endl;
}