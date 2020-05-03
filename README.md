# Lara

An interpretted language I'm working on with the help of my [language tools](https://github.com/NuriAmari/Language-Tools). Still very much a work in progress, but I've just finished function calls, including closures!

```python
let a = 2;

func test(a, b) {
    let c = 1;
    func add(a,b) {
        return a + b + c;
    }
    return add(a, b);
    print(1);
}

print(test(1, 1));
```
