from datetime import datetime as dt
import glob
import logging


def prep_logger(log_prefix: str, log_dir: str = 'logs'):
    existing_logs = glob.glob(log_dir+'/*.log')
    log_name = f'{log_prefix}_log_{dt.now().year}-{dt.now().month}-{dt.now().day}.log'
    exists = True
    exist_count = 1
    while exists:
        if log_name in [log.split('\\')[-1] for log in existing_logs]:
            log_name = (
                f'{log_prefix}_log_{dt.now().year}-{dt.now().month}-'
                f'{dt.now().day}({exist_count}).log'
                )
            exist_count += 1
        else:
            exists = False
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    f_handler = logging.FileHandler(f'{log_dir}/{log_name}')
    f_format = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    # keep_fds = [f_handler.stream.fileno()]

    return logger
