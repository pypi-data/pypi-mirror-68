# Codewars Test Framework for Python

## See also

This is a fork from https://github.com/Codewars/python-test-framework

## Example

```python
from solution import add
import codewars_test as test

@test.describe('Example Tests')
def example_tests():
    @test.it('Example Test Case')
    def example_test_case():
        test.assert_equals(add(1, 1), 2, 'Optional Message on Failure')
```
