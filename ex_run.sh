## path to a (patched) clipper
clipper="/home/zinzin2312/repos/clipper/clipper-distribution/target/clipper/clipper.sh"
nmo="/home/zinzin2312/repos/nemo/target/release/nmo"
rls="code/nemo/t_closure.rls"
fastdownward="/home/zinzin2312/repos/downward/fast-downward.py"
compiler="code/compiler.py"
tseitin="code/tseitin.py"
owl="benchmarks/cat/original/example.owl"

input_domain="benchmarks/cat/original/example_domain.pddl"
input_problem="benchmarks/cat/original/example_problem.pddl"
output_domain="benchmarks/outputs/cat/example_domain.pddl"
output_problem="benchmarks/outputs/cat/example_problem.pddl"

python3 "$compiler" "$owl" "$input_domain" "$input_problem" -d "$output_domain" -p "$output_problem" --clipper "$clipper" --clipper-mqf  --rls "$rls" --nmo "$nmo"

timeout 600 $fastdownward $output_domain $output_problem --search "let(hcea,cea(),lazy_greedy([hcea],preferred=[hcea]))"
