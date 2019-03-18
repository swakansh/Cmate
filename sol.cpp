#include <iostream>
#include <set>
#include <string>
#include <vector>

using namespace std;

template <class T>
vector<T> Vec(size_t l, T v) { return vector<T>(l, v); }

template <class T, class... Ts>
auto Vec(size_t l, Ts... ts) {
    return vector<decltype(Vec<T>(ts...))>(l, Vec<T>(ts...));
}

class ModInt {
    using ll = long long;

public:
    int value;
    static int MOD;

    ModInt(ll value = 0) {
        this->value = value % MOD;
        if (this->value < 0) this->value += MOD;
    }

    operator int() const noexcept { return this->value; }

    ModInt& operator=(const ModInt& x) {
        if (this != &x) { this->value = x.value; }
        return *this;
    }

    bool operator==(const ModInt& x) const { return this->value == x.value; }
    bool operator!=(const ModInt& x) const { return !(*this == x); }

    ModInt operator+() const { return value; }
    ModInt operator-() const { return MOD - value; }
    ModInt operator~() const { return (*this) ^ ModInt(MOD - 2); }

    ModInt operator++() { return *this += 1; }
    ModInt operator--() { return *this -= 1; }

    ModInt operator++(int) {
        ModInt before = *this;
        ++(*this);
        return before;
    }
    ModInt operator--(int) {
        ModInt before = *this;
        --(*this);
        return before;
    }

    ModInt operator+=(const ModInt& x) {
        int sum = this->value + x.value;
        return *this = (sum < MOD ? sum : sum - MOD);
    }
    ModInt operator-=(const ModInt& x) {
        int diff = this->value - x.value;
        return *this = (diff >= 0 ? diff : diff + MOD);
    }
    ModInt operator*=(const ModInt& x) { return *this = ll(this->value) * ll(x.value) % MOD; }
    ModInt operator/=(const ModInt& x) { return *this = (this->value % x.value == 0 ? ModInt(this->value / x.value) : *this * ~x); }

    ModInt operator+=(const int& x) {
        int sum = this->value + x;
        return *this = (sum < MOD ? sum : sum - MOD);
    }
    ModInt operator-=(const int& x) {
        int diff = this->value - x;
        return *this = (diff >= 0 ? diff : diff + MOD);
    }
    ModInt operator*=(const int& x) { return *this = ll(this->value) * ll(x) % MOD; }
    ModInt operator/=(const int& x) { return *this = (this->value % x == 0 ? ModInt(this->value / x) : *this * ~ModInt(x)); }

    template <class T>
    ModInt operator^=(const T& x) {
        int n = int(x);
        if (n == 0) return ModInt(1);
        if (n & 1) {
            return (*this) = ((*this) ^ ModInt(n - 1)) * (*this);
        } else {
            return (*this) = ((*this) * (*this)) ^ ModInt(n / 2);
        }
    }

    template <class T>
    ModInt operator+(const T& b) const { return ModInt(*this) += b; }
    template <class T>
    ModInt operator-(const T& b) const { return ModInt(*this) -= b; }
    template <class T>
    ModInt operator*(const T& b) const { return ModInt(*this) *= b; }
    template <class T>
    ModInt operator/(const T& b) const { return ModInt(*this) /= b; }
    template <class T>
    ModInt operator^(const T& b) const { return ModInt(*this) ^= b; }
};

int ModInt::MOD = 998244353;

ostream& operator<<(ostream& os, const ModInt& x) { return os << x.value; }
istream& operator>>(istream& is, ModInt& x) { return is >> x.value; }

void dfs(string S, set<string>& s) {
    if (s.count(S)) return;
    s.insert(S);
    for (int i = 0; i < S.size() - 1; ++i) {
        if (S[i] == S[i + 1]) continue;
        for (char c = 'a'; c <= 'c'; ++c) {
            if (S[i] != c && S[i + 1] != c) {
                string tmp = S;
                tmp[i] = tmp[i + 1] = c;
                dfs(tmp, s);
            }
        }
    }
}

int main() {
    string S;
    cin >> S;
    int N = S.size();

    if (set<char>(S.begin(), S.end()).size() == 1) {
        cout << 1 << endl;
        return 0;
    }

    if (S.size() <= 3) {
        set<string> s;
        dfs(S, s);
        cout << s.size() << endl;
        return 0;
    }

    int sum = 0;
    for (char c : S) sum += c - '0';
    sum %= 3;

    auto dp = Vec<ModInt>(N, 3, 3, 2, ModInt(0));

    dp[0][0][0][0] = dp[0][1][1][0] = dp[0][2][2][0] = 1;
    for (int i = 0; i < N - 1; ++i) {
        for (int c = 0; c < 3; ++c) {
            for (int m = 0; m < 3; ++m) {
                dp[i + 1][(m + c) % 3][c][0] += dp[i][m][(c + 1) % 3][0] + dp[i][m][(c + 2) % 3][0];
                dp[i + 1][(m + c) % 3][c][1] += dp[i][m][c][0] + dp[i][m][c][1] + dp[i][m][(c + 1) % 3][1] + dp[i][m][(c + 2) % 3][1];
            }
        }
    }

    ModInt ans = 1;
    for (int c = 0; c < 3; ++c) {
        ans += dp[N - 1][sum][c][1];
    }

    for (int i = 0; i < N - 1; ++i) {
        if (S[i] == S[i - 1]) {
            --ans;
            break;
        }
    }

    cout << ans << endl;
    return 0;
}
