This is a black-box fuzzer of the TeX unix binary.
This fuzzer is based on the paper [Fuzzing with Fast Failure Feedback](https://arxiv.org/pdf/2012.13516.pdf).
The source code project is [bFuzzer](https://github.com/vrthra/bFuzzer).

The fuzzer produces random, but syntactically-valid Tex inputs. 

First, make sure you have texlive installed in your linux machine. The wrapper that maps TeX error messages to the appropriate exit codes in implemented in `simplechains\tex\tex_fuzzer.py`

To remove results of previous runs, run:

  make clean

To run the fuzzer, execute:

  make fuzz_tex

The default run time is 3600 seconds (1 hour). You can modify the run time and other configuations from `stateless\config.py`

The generated inputs are stored in `valid_inputs.txt`

Below is an example of a generated Tex input


``` 
q $8S J$Ab8\it{I ls@y}!"-$,0.Z*fj\rightleftharpoons $$($L~A$ kkA_( mH"  UFGb$7c$P!($U$ X$V$/yG$bCt$\lambda $Q X$ vt,` 5^   \bigtriangledown IS\phi $$\min  $UhE8$g\partial{az}P _                  \firstmark{}$2 $d A$$VN\to{ V}n+B$$VZj/V*+ g$7OJ*`g$hD8xio 2p\propto iAef$+!$e5u $A ,fHuS>  ]\tenit{6z "gc$\ldotp J \footnote{d[v6a}v-o8|$o)7$p${o F}wl $Y$sMsy:;$lX!)v$ f\upbracefill{},1AQpN$va{o  2 N}wTR(99gX7/Mr1; f *$x][`oi\plainoutput Fk$a$Yx$@$x}
\end
``` 
