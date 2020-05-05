# Lara

An interpretted language I'm working on with the help of my [language tools](https://github.com/NuriAmari/Language-Tools). Still very much a work in progress, but most fundamental structures have been implemented:

## Variables

Currently, the only literal values support are integers.

#### Declaration

```javascript
let a = 1;
let b = a;
let c = 2;
```

#### Mutation

```javascript
a = 5;
b = 15;
c = b - 5;
```

## Expressions

All the basic mathematic operators are supported, including parenthesis for controlling precedence. Exponents (`**`) are recognized by the lexer, but not in the parser / evaluator yet. Since the only supported type is an integer, division is integer division.

```javascript
let a = 1 + 2;
let b = a - 5;
let c = a * 2 + 4;
let d = a * (2 + 4);
let e = a / 5;
```

## Functions

#### Declaration

```javascript
func add(a,b) {
    return a + b;
}
```

#### Invocation

```javascript
add(1,1);
```
#### Closures

```javascript
func outer(a, b) {
    let c = 1;
    func inner(a,b) {
        return a + b + c;
    }
    return add(a, b);
}

outer(1,1);
```
## Control Flow

#### If Statements

```javascript
if (a) {
    print(a);
} elif (b) {
    print(b);
} else {
    print(c);
}
```

#### Return 

```javascript
func print_only_one(a,b) {
    print(1);
    return;
    print(2);
    print(3);
}

print_only_one();
```

## IO

```javascript
print(1 + 1);
```
### Todo

- Loops
- Arrays
- More types
- First class functions

## Usage

1. Clone the repo
2. Symlink `lara` to somewhere on your PATH
3. Make executable `chmod +x lara`
3. Execute programs like `lara test.lr` (Note this assumes python3 is default python version on your machine)
4. If python3 is not default, run the script explicitly `python3 lara test.lr`
