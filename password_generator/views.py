from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404

import math
import random
import string 

# Create your views here.
def password_generator(request):
    class PasswordGenerate:
        def __init__(self, len_password = 0):
            self.len_password = len_password
            self.password = ""
            self._all_letters = string.ascii_letters + string.digits + string.punctuation
            self._len_all_letters = len(self._all_letters)
        
        def generate(self):
            for _ in range(self.len_password):
                _ = random.randint(0, len(self._all_letters) - 1)
                self.password += self._all_letters[_]
            return self.password

        def entropy(self):
            self.len_password = len(set(i for i in self.password))
            entropy = math.log2(self._len_all_letters ** self.len_password)
            return round(entropy, 2)
    
    context = {"len_password": 8,
                "password_generated": None,
                "password_entropy": None,}
    
    if request.method == "POST":
        if "generate" in request.POST:
            len_password = request.POST["rangeValue"]
            len_password = int(len_password)

            password = PasswordGenerate(len_password)
            password_generated = password.generate()
            password_entropy = password.entropy()

            if 0 < password_entropy < 70:
                entropy_level = "Słabe hasło"
            elif 70 < password_entropy < 100:
                entropy_level = "Dobre hasło"
            else:
                entropy_level = "Znakomite hasło!"

            context = {"len_password": len_password,
                       "password_generated": password_generated,
                       "password_entropy": password_entropy,
                       "entropy_level": entropy_level,}
            print(request.POST)
            

    return render(request= request, template_name= 'password_generator/password_generator.html', context= context)