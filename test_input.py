#!/usr/bin/env python3

import subprocess
import os

input_str = 'G(backslash)bf{I(backslash)output{QpzLl$"(backslash)@nother{FCSz}(backslash)bfc(backslash)big{I@kl }-k$4 ;$|S(backslash)@cclv{(backslash)accent &Dp}P[@<$E.;029o XgK $M(backslash)above *  b(backslash)bf(backslash)bigSWny7(backslash)big 6!n.T. iG(backslash)${_PRAG5 a3f &}G 2(backslash)accenta(backslash)arg{  (backslash)halign{P1}Q8R(backslash)arg1(backslash)output{f(backslash)above{?~Z}H`9&  (backslash)halign <}  (backslash)arg 5(backslash)$ (backslash)widetilde ,t(backslash)mathbin (backslash)mathbin{1VHM>5kXO2&-}} 5(backslash)halign{*HK({L}D]F(backslash)big{}r}$(backslash)argy`(backslash)mathbin (backslash)above $ (backslash)bf $j[+O9(backslash)@cclv  $0:uX  s+X(backslash)@cclv(backslash)mathbin{VT3(backslash)@nother 3(backslash)above iJ45?, h"T(D(backslash)halign4d} ( nj(backslash)@cclv{z&[((backslash)mathbin{dA(backslash)mathbin{3g(backslash)widetilde}n2'

cmd = "echo '"+ input_str + "' | sudo tee test.tex && sed -i -e 's/(backslash)/\\\/g' test.tex && echo 'test.tex \\\end' | tex > test.log"
excode = os.system(cmd)

if excode != 0 and excode != 256:
    print("Exit code: " + str(excode))

