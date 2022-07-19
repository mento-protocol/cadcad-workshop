import logging
import time
import pandas as pd

def run(experiment):
    '''
    Definition:
    Run simulation
    '''
    logging.info("Running experiment")
    start_time = time.time()

    experiment.run()

    experiment_duration = time.time() - start_time
    logging.info(f"Experiment complete in {experiment_duration} seconds")

    logging.info("Post-processing results")

    df = pd.DataFrame(experiment.results)

    post_processing_duration = time.time() - start_time - experiment_duration
    logging.info(f"Post-processing complete in {post_processing_duration} seconds")

    return df, experiment.exceptions

