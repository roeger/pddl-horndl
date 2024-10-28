domain="cat"
prefix="benchmarks/$domain"

# path to a (patched) clipper
clipper="/home/zinzin2312/repos/clipper/clipper-distribution/target/clipper/clipper.sh"
nmo="/home/zinzin2312/repos/nemo/target/release/nmo"
rls="code/nemo/t_closure.rls"

# path to compiler.py
compiler="code/compiler.py"
tseitin="code/tseitin.py"

owl=$prefix/original/TTL.owl
input_domain=$prefix/original/domain.pddl

# cats: 6
# elevator: 15

for i in `seq 15 15`;
do
  input_problem="$prefix/original/${domain}Problem${i}.pddl"

  # where the result should be written to
  result_domain="benchmarks/outputs/$domain/domain_${i}.pddl"
  result_problem="benchmarks/outputs/$domain/problem_${i}.pddl"
  tseitin_domain="benchmarks/outputs/$domain/compiled_domain${i}.pddl"
  tseitin_problem="benchmarks/outputs/$domain/compiled_problem${i}.pddl"

  # run compilation
  # python3 "$compiler" "$owl" "$input_domain" "$input_problem" --clipper "$clipper" --clipper-mqf --debug -v $@

  python3 "$compiler" "$owl" "$input_domain" "$input_problem" -d "$result_domain" -p "$result_problem" --clipper "$clipper" --clipper-mqf  --rls "$rls" --nmo "$nmo" --debug -v $@

  # run tseitin transformation
  # python3 "$tseitin" "$result_domain" "$result_problem" -d "$tseitin_domain" -p "$tseitin_problem" -v $@
done

rm -rf __temp_clipper_*

