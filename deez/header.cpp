#include <iostream>
#include <functional>
#include <vector>
#include <cassert> 

using namespace std;

class var{
	public:
		int type;
		float f;
		std::vector<var> __iter__;
		std::string s;
		std::function<var(var)> __exec__;

		var* _keys;
		var* _values;
		/*
		TYPEID | TYPE
		0 NULL
		1 INT   //removed, everything is a float
		2 FLOAT
		3 STRING
		4 BOOL
		5 LIST
		6 FUNCTION
		*/

		explicit var(int x, int t){
			this->type = t;
			this->f = (float)x;
		}

		explicit var(int x){
			this->type = 2;
			this->f = (float)x;
		}

		explicit var(float x){
			this->type = 2;
			this->f = (float)x;
		}

		explicit var(std::string s){
			this->type = 3;
			this->s = s;
		}

		explicit var(std::function<var(var)> f){
			this->type = 6;
			this->__exec__ = f;

		}
		
		explicit var(bool x){
			this->type = 4;
			this->f = (int)x;
		}
		

		explicit var(std::initializer_list<var> arr){

			for(var i: arr){
				this->__iter__.push_back(i);
			}
			this->type = 5;

		}

		std::string __repr__(){
			if     (this->type == 0){return "null";}                       // null
			//else if(this->type == 1){return std::to_string((int)this->f);} // int
			else if(this->type == 2){                                      // int / float
				if( this->f == ((int)(float)this->f)){
					return std::to_string((int)this->f);	
				}
				return std::to_string(this->f);
			}
			else if(this->type == 3){return this->s;}                      // string
			else if(this->type == 4){return std::to_string((bool)this->f);}// bool
			else if(this->type == 6){return "<function>";}                 // func
			else if(this->type == 5){
				string o = "[";
				for( var i:__iter__ ){
					o = o + i.__repr__() + ", ";
				}o.pop_back();o.pop_back();
				return o+"]";
			}															   // list[]
			else{return "unknown type "+std::to_string(this->type);}       // *unknown
		}

		var __getitem__(var x, var y = var(0,0)){
			if(this->type == 5 && x.type == 2){
				if(x.f < this->__iter__.size()){
					return this->__iter__.at((int)x.f);
				}return y;
			}return var(0, 0);
		}

		var __setitem__(var x, var v){
			if(this->type == 5 && x.type == 1){
				if((int)x.f < this->__iter__.size()){
					this->__iter__[(int)x.f] = v;
				}
			}return var(0, 0);
		}

		/*
		var __getattr__(var attr){
			assert(attr.type == 3);
			int c =0;
			for (auto i = this->_keys->__iter__.begin(); i != this->_keys->__iter__.end(); ++i){
				if( i->s == attr.s){
					break;
				}
				c++;
			}
			assert(c < this->_keys->__iter__.size());
			return this->_values->__iter__[c];
		}
		var __setattr__(var attr, var val){
			assert(attr.type == 3);
			int c =0;
			for (auto i = this->_keys->__iter__.begin(); i != this->_keys->__iter__.end(); ++i){
				if( i->s == attr.s){
					break;
				}
				c++;
			}
			if(c < this->_values->__iter__.size()){
				this->_values->__iter__[c] = val;
			}
			else{
				this->_keys->__iter__.push_back(attr);
				this->_values->__iter__.push_back(val);
			}
			return var(0);
		}*/

		var operator + (var x){return this->__add__(x);}
		var operator - (var x){return this->__sub__(x);}
		var operator * (var x){return this->__mul__(x);}
		var operator < (var x){return this->__lt__(x);}
		var operator > (var x){return this->__gt__(x);}
		var operator % (var x){return this->__mod__(x);}
		var operator == (var x){return this->__eq__(x);}

		var __add__(var x){
			if((this->type==2 || this->type==1) && (x.type==2 || x.type==1)){
				if(this->type==1 || x.type==1){
					return var((int)(x.f + this->f));
				}
				else{
					return var(x.f + this->f);	
				}
			}
			else{
				return var(0, 0);
			}
		}

		var __sub__(var x){
			if((this->type==2 || this->type==1) && (x.type==2 || x.type==1)){
				if(this->type==1 || x.type==1){
					return var((int)(this->f - x.f));
				}
				else{
					return var(this->f - x.f);	
				}
			}
			else{
				return var(0, 0);
			}
		}

		var __mul__(var x){
			if((this->type==2 || this->type==1) && (x.type==2 || x.type==1)){
				if(this->type==1 || x.type==1){
					return var((int)(this->f * x.f));
				}
				else{
					return var(this->f * x.f);	
				}
			}
			else{
				return var(0, 0);
			}
		}

		var __eq__(var x){
			if(this->type == x.type){
				//cout<<this->f<<"=="<<x.f<<" ->"<< (this->f==x.f) <<endl;
				return var( this->f == x.f );
			}
			return var(0, 0);
		}

		var __lt__(var x){
			if(this->type == x.type){
				return var(this->f < x.f);
			}return var(0, 0);
		}

		var __gt__(var x){
			if(this->type == x.type){
				return var(this->f > x.f);
			}return var(0, 0);	
		}

		var __mod__(var x){
			if(this->type == x.type){
				float a = (float)this->f;
				float b = (float)x.f;
				float mod = a < 0 ? -a : a;

				while(mod >= b){
					mod = mod - b;
				}
				return a < 0 ? var(-mod) : var(mod);
			}return var(0, 0);
		}

		operator bool(){
			return (bool)(this->f)||(bool)(this->s.size())||this->__iter__.size();
		}

};


void print(var x){
	for(var i: x.__iter__){
		cout<<i.__repr__()<<" ";
	}
	cout<<endl;
}

var input(var a){
	var x = a.__iter__[0];
	std::string v;
	cout<< x.__repr__();
	cin >> v;
	return var(v);
}
var repr(var x){
	return var(x.__repr__());
}

int main(){
	%%main
}