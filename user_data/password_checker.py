from secrets import compare_digest
from string import digits



class PasswordChecker:
    def __init__(self, new_pass1: str, new_pass2: str):
        self.new_pass1: str = new_pass1
        self.new_pass2: str = new_pass2
        self.min_lenght: int = 8


    def compare_passwords(self) -> bool:
        return compare_digest(self.new_pass1, self.new_pass2)
    

    def not_only_numerical(self) -> bool:
        return not all([s in digits for s in self.new_pass1])
    

    def too_short(self) -> bool:
        return not len(self.new_pass1) >= self.min_lenght



if __name__ == "__main__":
    pass1 = PasswordChecker('412421421', '412421421')
    assert pass1.compare_passwords() is True
    assert pass1.not_only_numerical() is False
    assert pass1.too_short() is False

    pass2 = PasswordChecker('412421421', '4124214211')
    assert pass2.compare_passwords() is False
    assert pass2.not_only_numerical() is False
    assert pass2.too_short() is False

    pass3 = PasswordChecker('412421421gtdfsyhgfre', '412421421gtdfsyhgfre')
    assert pass3.compare_passwords() is True
    assert pass3.not_only_numerical() is True
    assert pass3.too_short() is False

    pass4 = PasswordChecker('hgfre', 'hgfre')
    assert pass4.compare_passwords() is True
    assert pass4.not_only_numerical() is True
    assert pass4.too_short() is True