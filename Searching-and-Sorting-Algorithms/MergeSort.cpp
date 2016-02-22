#include <iostream>
#include <vector>
#include <math.h>

using namespace std;
int main(){
	return 1;
}

int sorting(vector<int> vector3){
	int test = vector3.size();
	if(test>1){

		int middle = floor(test / 2);
		vector<int> left = vector3.resize(middle);
		int right = ;


		vector<int> left = vector3.resize(middle);
		vector<int> right = vector3.resize(middle);

		sorting(left);
		sorting(right);

		int a = 0;
		int b = 0;
		int c = 0;

		while (a < left.size() && b < right.size()){

			if (left[a] < right[b]){
				vector3[c] = left[a];
				a += 1;
			}
			else{
				vector3[c] = right[b];
				b += 1;
			c+=1;
			}
		while (a <left.size()){
			vector3[c] = left[a];
			a += 1;
			c += 1;
		}
		}
		while (b < right.size()){
			vector3[c] = right[b];
			b += 1;
			c += 1;
		}

	}

	return 0;
}
