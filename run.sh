domain="cats"
prefix="benchmarks/$domain"

# path to a (patched) clipper
clipper="/home/zinzin2312/repos/clipper/clipper-distribution/target/clipper/clipper.sh"
nmo="/home/zinzin2312/repos/nemo/target/release/nmo"
rls="code/nemo/t_closure.rls"

# path to compiler.py
compiler="code/compiler.py"
tseitin="code/tseitin.py"

for i in `seq 6 6`;
do
  owl=$prefix/original/TTL.owl
  input_domain=$prefix/original/domain.pddl
  input_problem="$prefix/original/catProblem${i}.pddl"

  # where the result should be written to
  result_domain="benchmarks/outputs/$domain/domain_${i}.pddl"
  result_problem="benchmarks/outputs/$domain/problem_${i}.pddl"
  tseitin_domain="benchmarks/outputs/$domain/compiled_domain_${i}.pddl"
  tseitin_problem="benchmarks/outputs/$domain/compiled_problem${i}.pddl"

  # run compilation
  # python3 "$compiler" "$owl" "$input_domain" "$input_problem" --clipper "$clipper" --clipper-mqf --debug -v $@

  python3 "$compiler" "$owl" "$input_domain" "$input_problem" -d "$result_domain" -p "$result_problem" --clipper "$clipper" --clipper-mqf  --rls "$rls" --nmo "$nmo" --debug -v $@

  # python3 pddl-horndl/code/tseitin.py pddl-horndl/benchmarks/cats/original/TTL.owl pddl-horndl/benchmarks/cats/original/domain.pddl /pddl-horndl/benchmarks/cat/soriginal/catProblem6.pddl -d --clipper /home/zinzin2312/repos/clipper/clipper-distribution/target/clipper/clipper.sh --clipper-mqf --debug -v

  # run tseitin transformation
  # python3 "$tseitin" "$result_domain" "$result_problem" -d "$tseitin_domain" -p "$tseitin_problem" -v $@
done

rm -rf __temp_clipper_*

