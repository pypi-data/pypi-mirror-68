# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdklinkedmall.endpoint import endpoint_data

class CreatePayUrlRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'linkedmall', '2018-01-16', 'CreatePayUrl','linkedmall')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_BizUid(self):
		return self.get_query_params().get('BizUid')

	def set_BizUid(self,BizUid):
		self.add_query_param('BizUid',BizUid)

	def get_UseAnonymousTbAccount(self):
		return self.get_query_params().get('UseAnonymousTbAccount')

	def set_UseAnonymousTbAccount(self,UseAnonymousTbAccount):
		self.add_query_param('UseAnonymousTbAccount',UseAnonymousTbAccount)

	def get_BuyInfo(self):
		return self.get_body_params().get('BuyInfo')

	def set_BuyInfo(self,BuyInfo):
		self.add_body_params('BuyInfo', BuyInfo)

	def get_ThirdPartyUserId(self):
		return self.get_query_params().get('ThirdPartyUserId')

	def set_ThirdPartyUserId(self,ThirdPartyUserId):
		self.add_query_param('ThirdPartyUserId',ThirdPartyUserId)

	def get_BizId(self):
		return self.get_query_params().get('BizId')

	def set_BizId(self,BizId):
		self.add_query_param('BizId',BizId)