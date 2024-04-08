import unittest
import os
import shutil
import zipfile
from unitTests import TestAPIEndpoints
from datetime import datetime

def suite():
    suite = unittest.TestSuite()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAPIEndpoints)
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())

    # Write results to a file
    result_file_name = 'test_results.txt'
    with open(result_file_name, 'w') as result_file:
        result_file.write('Errors:\n')
        result_file.write('\n'.join(map(str, result.errors)) + '\n\n')
        result_file.write('Failures:\n')
        result_file.write('\n'.join(map(str, result.failures)) + '\n\n')
        result_file.write('Successes:\n')
        result_file.write('Tests run: %s\n' % result.testsRun)
        successes = result.testsRun - len(result.failures) - len(result.errors)
        result_file.write('Successes: %s\n' % successes)

    # Create a zip file with the current date and time
    zip_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_test_results.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(result_file_name)

    # Create 'test results' folder if it doesn't exist
    test_results_dir = 'test_results'
    os.makedirs(test_results_dir, exist_ok=True)

    # Move the zip into the 'test results' folder
    shutil.move(zip_filename, os.path.join(test_results_dir, zip_filename))

    # Delete the original result file
    os.remove(result_file_name)
