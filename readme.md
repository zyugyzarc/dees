# Deez
Deez is a compiled, dynamicaly typed, programming language made with C++ and Python.

## Quickstart
(using the js syntax hilighter works well enough for this)
```js
fizzbuzz(n)->{
	for( i=1 )( i<n )( i=i+1 ){
		
		if( i%3==0 and i%5 == 0 ){
			print("fizzbuzz")
		}else if( i%3 ==0 ){
			print("fizz")
		}else if( i%5 == 0){
			print("buzz")
		}else{
			print(i)
		}
	}
}

fizzbuzz(20)
```

####Note: requires `g++`

### Installation
* install python 3.6 or above
* install `g++`
* install deez `pip install git+https://github.com/zyugyzarc/deez.git`

### Usage
you can compile your scripts by doing  
`python3 -m deez myfile.deez`  
(`.deez` is the file extension for deez scripts.)

## Reference

### Types
* number (integer or float)
* string
* bool
* null
* function
* *list \[experimental, not implemented\]*

### Variables

variables can be created similar to the following:  
`x = 0`  
`b = false`  
`foo = "Hello"`  
`bar = 'Hello'`  
`baz = null`  


### Statements

the following statements work as given:
```js
if( ... ){
	//do something
}else if( ... ){
	//do something else
}else{
	//do something else else
}
```

```js
i = 0
while(i < 10){
	//do something
	i = i + 1
}
```

```js
for (i = 0)(i < 10)(i = i+1){
	//do something
}
```

### Operators
the following operators have been implemented  
* addition (`x + y`) 
* subtraction (`x - y`)
* multiplication (`x * y`)
* greater than (`x > y`)
* less than (`x < y`) 
* equal to (`x == y`)
* modulo (`x % y`)

### Functions

functions can be defined as such
```js
func(x)->{
	print("Hello ", x)
}
```
and called by  
`func("Joe")`

recursive functions also work:
```js
fact(x)->{
	if( x==0 ){
		return 1
	}
	return x * fact(x-1)
}
```

you can also use lambdas or inline functions.
```js
//this is an inline function
(x)->{ print("Hello", x) } 
```
and can be used to define functions normally
```js
func = (x)->{ print("Hello", x) }
```
