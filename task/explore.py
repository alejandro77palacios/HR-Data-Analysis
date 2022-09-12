import os

import pandas as pd
import requests

# scroll down to the bottom to implement your solution

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.
    office_a = pd.read_xml('../Data/A_office_data.xml', parser='etree')
    office_b = pd.read_xml('../Data/B_office_data.xml', parser='etree')
    hr = pd.read_xml('../Data/hr_data.xml', parser='etree')

    office_a.set_index('employee_office_id', inplace=True)
    office_a.index = 'A' + office_a.index.astype('str')

    office_b.set_index('employee_office_id', inplace=True)
    office_b.index = 'B' + office_b.index.astype('str')

    hr.set_index('employee_id', inplace=True)

    office = pd.concat([office_a, office_b])
    fusion = office.merge(hr, left_index=True, right_index=True, how='left', indicator=True)
    fusion = fusion[fusion['_merge'] == 'both']

    fusion.drop(columns=['_merge'], inplace=True)
    fusion.sort_index(inplace=True)

    fusion.left = fusion.left.astype(int)

    first_pivot = fusion.pivot_table(index='Department', columns=['left', 'salary'], values='average_monthly_hours',
                                     aggfunc='median')
    second_pivot = fusion.pivot_table(index='time_spend_company',
                                      columns='promotion_last_5years',
                                      values=['satisfaction_level', 'last_evaluation'],
                                      aggfunc=['min', 'max', 'mean'])
    first_filter = first_pivot.loc[(first_pivot[(0, 'high')] < first_pivot[(0, 'medium')]) &
                    (first_pivot[(1, 'low')] < first_pivot[(1, 'high')])]
    second_filter = second_pivot.loc[second_pivot[('mean', 'last_evaluation', 0)] > second_pivot[('mean', 'last_evaluation', 1)]]

    first_dict = first_filter.round(2).to_dict()
    second_dict = second_filter.round(2).to_dict()
    print(first_dict)
    print(second_dict)


