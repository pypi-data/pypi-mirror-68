# See LICENSE.incore for license details
import logging
import os
import shutil
import sys

import repomanager
import repomanager.utils as utils
import repomanager.rpm as repoman

def main():
    '''
        Entry point for riscv_config.
    '''

    # Set up the parser
    parser = utils.cmdline_args()
    args = parser.parse_args()

    # Set up the logger
    utils.setup_logging(args.verbose)
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(utils.ColoredFormatter())
    logger.addHandler(ch)

    logger.info('################### Repository Manager ##################')
    logger.info('--- Copyright (c) 2020 InCore Semiconductors Pvt. Ld. ---')
    logger.info('------------------- Version : {0} ---------------------'.format(repomanager.__version__))
    logger.info('#########################################################')
    logger.info('\n')

    repoman.repoman(args.yaml, args.clean, args.update, args.patch,
            args.unpatch, args.dir)

if __name__ == "__main__":
    exit(main())
