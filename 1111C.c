#include<stdio.h>
#include<stdlib.h>

int n, k, A, B;
int a[100000 + 7];

long long my_min(long long x, long long y){
	if(x < y){
		return x;
	}
	return y;
}

int find(int x){
	int r = k - 1, l = 0;
	if(x > a[r]){
		return k;
	}
	if(x <= a[0]){
		return 0;
	}
	while(1){
		if(r - l == 1){
			break;
		}
		if(x > a[(r + l) / 2]){
			l = (r + l) / 2;
		}
		else{
			r = (r + l) / 2;
		}
	}
	return r;
}

long long Des(int l, int r){
	int length = r - l;
	int n_a = find(r) - find(l);
	
	if(n_a == 0){
		return A;
	}
	if(length == 1){
		return (long long)B*n_a*length;
	}
	return my_min((long long)B*n_a*length, Des(l, l+length/2)+Des(l+length/2, r));
}

int com(const void *x, const void *y){
	int *a = (int*)x;
	int *b = (int*)y;
	return *a-*b;
}

int main(void){
	scanf("%d %d %d %d", &n, &k, &A, &B);
	for(int i = 0; i < k; i++){
		scanf("%d", &a[i]);
	}
	qsort(a, k, sizeof(int), com);
	printf("%lld\n", Des(1, (1<<n) + 1));
}