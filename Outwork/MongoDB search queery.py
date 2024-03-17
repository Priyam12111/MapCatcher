from pymongo import MongoClient
from urllib.parse import quote_plus
from pymongo import UpdateOne
import io
import csv
from datetime import datetime, timedelta
from itertools import islice

# Replace <username>, <password>, and <cluster-url> with your MongoDB Atlas credentials
username = "manojtomar326"
password = "Tomar@@##123"
cluster_url = "cluster0.ldghyxl.mongodb.net"

# Encode the username and password using quote_plus()
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

client = MongoClient("mongodb+srv://Priyam:5H7SatQX2vjV60ea@mapcasher.fkurktv.mongodb.net/")
db = client["MapData"]
collection = db['Mapcollection']

# Conditionally set the value of a new field
filter_query = {}

# '''Normal Match'''
# update_query = [
#     {
#         '$set': {
#             'data_dict': {
#                 '$map': {
#                     'input': '$data_dict',
#                     'in': {
#                         '$mergeObjects': [
#                             '$$this',
#                             {
#                                 'Department': {
#                                     '$cond': [
#                                         { '$in': ['$$this.designation', ['CMO', 'Advertising', 'SEO', 'Ad', 'Demand', 'Social Media', 'Campaign', 'Affiliate', 'Brand', 'Kampagnen', 'Channel', 'Website', 'Social', 'Communication', 'User Acquisition', 'Martech', 'PR', 'Marketing', 'Market Research']] },
#                                         'Marketing',
#                                         {
#                                             '$cond': [
#                                                 { '$in': ['$$this.designation', ['Procurement', 'Sourcing', 'Vendor', 'Purchase']] },
#                                                 'Vendor',
#                                                 {
#                                                     '$cond': [
#                                                         { '$in': ['$$this.designation', ['Human', 'Resource', 'People', 'HR', 'Talent', 'Acquisition', 'Recruiter', 'Culture', 'HRIS (Human Resource Information System)', 'HR Manager']] },
#                                                         'HR',
#                                                         {
#                                                             '$cond': [
#                                                                 { '$in': ['$$this.designation', ['Business', 'Sales', 'Growth', 'Customer', 'Community', 'Partnerships', 'Success', 'Client', 'Development']] },
#                                                                 'Sales',
#                                                                 {
#                                                                     '$cond': [
#                                                                         { '$in': ['$$this.designation', ['Project', 'Product', 'Production', 'Content', 'Localization', 'Operations', 'Video', 'Editor', 'Digital']] },
#                                                                         'Operation',
#                                                                         {
#                                                                             '$cond': [
#                                                                                 { '$in': ['$$this.designation', ['Finance', 'Account', 'Payments', 'Accountant', 'Financial', 'Audit', 'Tax', 'Payroll']] },
#                                                                                 'Account',
#                                                                                 {
#                                                                                     '$cond': [
#                                                                                         { '$in': ['$$this.designation', ['Creative', 'Strategy', 'Strategist', 'Analysis', 'Strategic', 'Corporate Development']] },
#                                                                                         'Strategy',
#                                                                                         'Exclude'
#                                                                                     ]
#                                                                                 }
#                                                                             ]
#                                                                         }
#                                                                     ]
#                                                                 }
#                                                             ]
#                                                         }
#                                                     ]
#                                                 }
#                                             ]
#                                         }
#                                     ]
#                                 }
#                             }
#                         ]
#                     }
#                 }
#             }
#         }
#     }
# ]



# '''Lower Match'''

# update_query = [
#     {
#         '$set': {
#             'Department': {
#                 '$cond': [
#                     { '$in': [{ '$toLower': '$data_dict.designation' }, ['cmo', 'advertising', 'seo', 'ad', 'demand', 'social media', 'campaign', 'affiliate', 'brand', 'kampagnen', 'channel', 'website', 'social', 'communication', 'user acquisition', 'martech', 'pr', 'marketing', 'market research']] },
#                     'Marketing',
#                     {
#                         '$cond': [
#                             { '$in': [{ '$toLower': '$data_dict.designation' }, ['procurement', 'sourcing', 'vendor', 'purchase']] },
#                             'Vendor',
#                             {
#                                 '$cond': [
#                                     { '$in': [{ '$toLower': '$data_dict.designation' }, ['human', 'resource', 'people', 'hr', 'talent', 'acquisition', 'recruiter', 'culture', 'hris (human resource information system)']] },
#                                     'HR',
#                                     {
#                                         '$cond': [
#                                             { '$in': [{ '$toLower': '$data_dict.designation' }, ['business', 'sales', 'growth', 'customer', 'community', 'partnerships', 'success', 'client', 'development']] },
#                                             'Sales',
#                                             {
#                                                 '$cond': [
#                                                     { '$in': [{ '$toLower': '$data_dict.designation' }, ['project', 'product', 'production', 'content', 'localization', 'operations', 'video', 'editor', 'digital']] },
#                                                     'Operation',
#                                                     {
#                                                         '$cond': [
#                                                             { '$in': [{ '$toLower': '$data_dict.designation' }, ['finance', 'account', 'payments', 'accountant', 'financial', 'audit', 'tax', 'payroll']] },
#                                                             'Account',
#                                                             {
#                                                                 '$cond': [
#                                                                     { '$in': [{ '$toLower': '$data_dict.designation' }, ['creative', 'strategy', 'strategist', 'analysis', 'strategic', 'corporate development']] },
#                                                                     'Strategy',
#                                                                     'None'
#                                                                 ]
#                                                             }
#                                                         ]
#                                                     }
#                                                 ]
#                                             }
#                                         ]
#                                     }
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             }
#         }
#     }
# ]


# '''Partially Match'''
update_query = [
    {
        '$set': {
            'data_dict': {
                '$map': {
                    'input': '$data_dict',
                    'in': {
                        '$mergeObjects': [
                            '$$this',
                            {
                                'Department': {
                                    '$cond': [
                                        { '$regexMatch': { 'input': '$$this.designation', 'regex': 'CMO|Advertising|SEO|Ad|Demand|Social Media|Campaign|Affiliate|Brand|Kampagnen|Channel|Website|Social|Communication|User Acquisition|Martech|PR|Marketing|Market Research', 'options': 'i' } },
                                        'Marketing',
                                        {
                                            '$cond': [
                                                { '$regexMatch': { 'input': '$$this.designation', 'regex': 'Procurement|Sourcing|Vendor|Purchase', 'options': 'i' } },
                                                'Vendor',
                                                {
                                                    '$cond': [
                                                        { '$regexMatch': { 'input': '$$this.designation', 'regex': 'Human|Resource|People|HR|Talent|Acquisition|Recruiter|Culture|HRIS (Human Resource Information System)', 'options': 'i' } },
                                                        'HR',
                                                        {
                                                            '$cond': [
                                                                { '$regexMatch': { 'input': '$$this.designation', 'regex': 'Business|Sales|Growth|Customer|Community|Partnerships|Success|Client|Development', 'options': 'i' } },
                                                                'Sales',
                                                                {
                                                                    '$cond': [
                                                                        { '$regexMatch': { 'input': '$$this.designation', 'regex': 'Project|Product|Production|Content|Localization|Operations|Video|Editor|Digital', 'options': 'i' } },
                                                                        'Operation',
                                                                        {
                                                                            '$cond': [
                                                                                { '$regexMatch': { 'input': '$$this.designation', 'regex': 'Finance|Account|Payments|Accountant|Financial|Audit|Tax|Payroll', 'options': 'i' } },
                                                                                'Account',
                                                                                {
                                                                                    '$cond': [
                                                                                        { '$regexMatch': { 'input': '$$this.designation', 'regex': 'Creative|Strategy|Strategist|Analysis|Strategic|Corporate Development', 'options': 'i' } },
                                                                                        'Strategy',
                                                                                        'None'
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
]


collection.update_many(filter_query, update_query)

# Close the MongoDB connection
client.close()
