```bash
[bennet@skills:~/snakemake/ibic]$ snakemake help
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	help
	1

Job 0: 

The available rules for this Snakefile are:
       bet               Skull strip
       mcflirt           Motion correction for resting state
       mean_func         Create one-volume mean activity image
       register_motion   Register motion-corrected functional data
                         to anatomical scan
       all               Run all of the above

        

Finished job 0.
1 of 1 steps (100%) done

[bennet@skills:~/snakemake/ibic]$ snakemake all
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	all
	1	bet
	1	mean_func
	1	motion
	1	register_motion
	5

rule motion:
    input: rest.nii.gz
    output: rest_mc.nii.gz
    jobid: 4

Finished job 4.
1 of 5 steps (20%) done

rule mean_func:
    input: rest_mc.nii.gz
    output: rest_mean_func.nii.gz
    jobid: 3

Finished job 3.
2 of 5 steps (40%) done

rule bet:
    input: T1.nii.gz
    output: T1_skstrip.nii.gz
    jobid: 2

Finished job 2.
3 of 5 steps (60%) done

rule register_motion:
    input: rest_mean_func.nii.gz, T1_skstrip.nii.gz
    output: xfm_dir/rest_to_T1.nii.gz
    jobid: 1

Finished job 1.
4 of 5 steps (80%) done

localrule all:
    input: xfm_dir/rest_to_T1.nii.gz
    jobid: 0

Finished job 0.
5 of 5 steps (100%) done
```
