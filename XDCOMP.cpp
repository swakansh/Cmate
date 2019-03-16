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

// Upsolving

// Approach:

// DP

// See if the tree will be split such that each part has xor x then either the tree will be split in
// even number of parts or odd number of parts. OK?

// So if the whole of the tree has xor zero then it needs to be split in even number of parts
// and if xor of the tree is x then it needs to be split in odd number of parts. OK?

// If the xor of the tree is neither zero nor x then there exist no solutions.

// Now, 
 
// Let's maintain a 2d dp(dp[u][2]) that will store the number of ways to split the subtree rooted at node u 
// such that index 0 stores number of ways to split the subtree into even number of parts each giving xor x
// index 1 stores number of ways to split the subtree into odd number of parts each giving xor x.
// Using this dp we can calculate the answer for parent node.

// How ?
// Suppose for a subtree you know the number of ways of even and odd number of split when there exists 
// solution for this subtree then what will be the transitions?

// let dp[to][0] denote number of ways to solve for child to of node u (with even number of subparts)
// and dp[to][1] with odd number of subparts

// then we have two choices either to take this edge (the one connecting with child to) or not

// // When we take this edge
// dp[u][0] = dp[to][0] * dp[u][1] + dp[to][1] * dp[u][0];
// In order to have overall even number of subparts for node u take even number of subparts from node already 
// available solution and take odd number of subparts from child solution 
// so then overall
//     even - 1 + odd - 1 + 1 == even

// similarly
//     odd - 1 + even - 1 + 1 == odd

// One part from each part combine to become 1 

// and similarly to have odd number of parts take even from already available and even from child and 

// combine them to have odd number of parts or odd from both parts


// When we don't take this edge then also we can figure out the cases but we have to take care of the fact that
// the child should have the solution for its subtree, that is, it should be possible to split this child subtree to 
// give xor x.



#define N 100002
int64 a[N], x;
vector<int> g[N];
int64 ans[N][2], dp[N][2], xors[N];
void dfs(int u, int p){
    dp[u][0] = 0;
    dp[u][1] = 1;
    xors[u] ^= a[u - 1];
    for(int to : g[u]){
        if(to == p) continue;
        dfs(to, u);
        xors[u] ^= xors[to];
        int64 temp[2] = {0};
        
        //edge is not deleted
        temp[0] += (dp[to][0] * dp[u][1]) % mod + (dp[to][1] * dp[u][0]) % mod;
        temp[0] %= mod;
        temp[1] += (dp[to][1] * dp[u][1]) % mod + (dp[to][0] * dp[u][0]) % mod;
        temp[1] %= mod;
        
        //edge is deleted
        temp[0] += (ans[to][0] * dp[u][0]) % mod + (ans[to][1] * dp[u][1]) % mod;
        temp[0] %= mod;
        temp[1] += (ans[to][1] * dp[u][0]) % mod + (ans[to][0] * dp[u][1]) % mod;
        temp[1] %= mod;
        
        dp[u][0] = temp[0];
        dp[u][1] = temp[1];
    }
    if(xors[u] == 0)    ans[u][0] = dp[u][0];
    if(xors[u] == x)    ans[u][1] = dp[u][1];
} 
int main(){
    FAST
    //Do awesome things here
    int n;
    cin >> n >> x;
    rp(i, n){
        cin >> a[i];
    }
    rp(i, n - 1){
        int u, v;
        cin >> u >> v;
        g[u].pb(v);
        g[v].pb(u);
    }
    dfs(1, -1);
    cout << (ans[1][0] + ans[1][1]) % mod << endl;
    return 0;
}


inline void measure(){
    auto stop = high_resolution_clock::now(); 
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << duration.count() << endl;
}