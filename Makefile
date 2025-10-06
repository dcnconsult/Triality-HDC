all: phi koopman latency

phi:
	python experiments/phi_vs_rational_metrics.py

koopman:
	python experiments/koopman_gap_metrics.py

latency:
	python experiments/latency_fit_metrics.py
