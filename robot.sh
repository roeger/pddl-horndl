clipper="/home/zinzin2312/repos/clipper/clipper-distribution/target/clipper/clipper.sh"
nmo="/home/zinzin2312/repos/nemo/target/release/nmo"
rls="code/nemo/t_closure.rls"
fastdownward="/home/zinzin2312/repos/downward/fast-downward.py"

compiler="code/compiler.py"
tseitin="code/tseitin.py"

# elements=(13 110 37 180 12 23 29 50 10 200 70 28 90 9 120 41 5 18 30 31 4 16 33 3 42 17 27 38 39 25 140 22 15 8 14 160 35 11 60 26 20 6 32 21 190 19 170 7 150 36 34 130 100 24 40 80)
elements=(10 9 5 4 3 8 11 6 7)
robotDir=benchmarks/robot/original

for i in ${elements[@]};
do
  owl=$robotDir/TTL${i}.owl
  input_domain=$robotDir/robotDomain${i}.pddl
  input_problem=$robotDir/robotProblem${i}.pddl

  result_domain="benchmarks/outputs/robot/domain_${i}.pddl"
  result_problem="benchmarks/outputs/robot/problem_${i}.pddl"
  tseitin_domain="benchmarks/outputs/robot/compiled_domain_${i}.pddl"
  tseitin_problem="benchmarks/outputs/robot/compiled_problem_${i}.pddl"

  python3 "$compiler" "$owl" "$input_domain" "$input_problem" -d "$result_domain" -p "$result_problem" --clipper "$clipper" --clipper-mqf  --rls "$rls" --nmo "$nmo" --debug $@ 2> "benchmarks/outputs/robot/compilations/time_${i}.txt"

  # run tseitin transformation and append the result to the file
  python3 "$tseitin" "$result_domain" "$result_problem" -d "$tseitin_domain" -p "$tseitin_problem" --keep-name $@ 2>> "benchmarks/outputs/robot/compilations/time_${i}.txt"

  echo "Solving problem $i"
  # timeout 600 $fastdownward $domain $problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])" > "benchmarks/outputs/$domain/solutions/solution${i}.txt" 2>&1
  timeout 600 $fastdownward $tseitin_domain $tseitin_problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])" > "benchmarks/outputs/robot/solutions/log_${i}.txt" 2>&1

done

rm -rf __temp_clipper_*
rm -rf sas_plan
