all: phi koopman latency
phi:
	python -m experiments.phi_vs_rational_metrics
koopman:
	python -m experiments.koopman_gap_metrics
latency:
	python -m experiments.latency_fit_metrics
ablations:
	python -m experiments.ablations
aggregate:
	python -m scripts.aggregate
full:
	make all && make ablations && make aggregate
