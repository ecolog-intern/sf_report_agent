SOQL_QUERY = """SELECT 
    Contractor_Information__r.Name,
    Contractor_Information__r.smart_customer_id__c,
    Name,
    plan_code__r.Name,
    Contractor_Information__r.parent_agency__c,
    Contractor_Information__r.account__c,
    Contractor_Information__r.sales_channel__c,
    Contractor_Information__r.customer_type__c,
    Contractor_Information__r.contractor_name__c,
    Contractor_Information__r.contractor_name_kana__c,
    Comp_Before_Switch__r.Name,
    current_power_plan__c,
    supply_point_identification_no__c,
    customer_no__c,
    latest_billing_year_month__c,
    bill__c,
    power_usage_kwh__c,
    contract_amps__c,
    contract_kvc__c,
    billing_amount__c,
    discount_rate__c,
    Contractor_Information__r.payment_type__c,
    place_name__c,
    Contractor_Information__r.zip__c,
    Contractor_Information__r.contractor_address__c,
    Contractor_Information__r.request_date__c,
    Contractor_Information__r.atokaku_call_status__c,
    contract_confirmation_call_ok_date__c,
    Contractor_Information__r.latest_billing_month__c,
    Contractor_Information__r.Latest_payment_meyhod__c,
    cancel_date__c,
    cancel_confirmed_date__c,
    cancellation_date__c,
    cancel_reason__c,
    use_place_zip__c,
    use_place_address_connect__c,
    use_place_name__c,
    use_place_name_kana__c,
    matching_result__c,
    switching_request_ok_date__c,
    scheduled_switching_date__c,
    Contractor_Information__r.email__c,
    Contractor_Information__r.business_sector__c,
    Contractor_Information__r.business_sector_detail__c,
    Contractor_Information__r.fact_clct_date__c,
    Contractor_Information__r.representative_age__c,
    Contractor_Information__r.representative_brth__c,
    Contractor_Information__r.representative_country__c,
    Contractor_Information__r.representative_name__c,
    Contractor_Information__r.representative_name_kana__c,
    Contractor_Information__r.pic_name__c,
    Contractor_Information__r.pic_name_kana__c,
    Contractor_Information__r.pic_tel__c,
    Contractor_Information__r.shop_name__c,
    distinguish_place_tel__c,
    Contractor_Information__r.tel1_connect__c,
    use_place_tel__c,
    Contractor_Information__r.tel2_connect__c,
    Contractor_Information__r.document_destination_name__c,
    Contractor_Information__r.document_destination_address_connect__c,
    remarks1__c,
    remarks2__c,
    remarks3__c,
    Contractor_Information__r.atokaku_comment__c,
    Contractor_Information__r.claim_linking_no__c,
    Contractor_Information__r.application_information__r.Name
FROM Electrical_Contract__c
WHERE 
    cancel_date__c = null
    AND cancel_reason__c = null
    AND cancel_confirmed_date__c = null
    AND cancel_cooperation_date__c = null
    AND forced_termination_date__c = null
    AND cancellation_confirmed_date__c = null
    AND cancellation_date__c = null
    AND Compulsory_cancellation_date__c = null
    AND Contractor_Information__r.parent_agency__c != '株式会社アイステーション（管理）'
    AND Contractor_Information__r.parent_agency__c != '株式会社アクセル（商品企画）'
    AND Contractor_Information__r.parent_agency__c != '株式会社ネクシィーズ'
    AND Contractor_Information__r.account__c != '株式会社ネクシィーズ'
    AND Contractor_Information__r.account__c != 'NUWORKS株式会社(t)'
    AND Contractor_Information__r.account__c != 'NUWORKS株式会社（テンポス）'
    AND Contractor_Information__r.account__c != '株式会社come up'
    AND Contractor_Information__r.Latest_payment_meyhod__c != 'コンビニ'
    AND Contractor_Information__r.Call_FLG__c = null
    AND Contractor_Information__r.parent_agency__c != 'EPARK（管理）'
    AND switching_request_ok_date__c != null
    AND scheduled_switching_date__c >= 2025-10-01
    AND scheduled_switching_date__c < 2025-11-01
ORDER BY scheduled_switching_date__c DESC"""

REPORT_META = {
  "aggregates": [
    "s!Electrical_Contract__c.contract_kvc__c",
    "s!Electrical_Contract__c.billing_amount__c",
    "s!Contractor_Information__c.representative_age__c",
    "RowCount"
  ],
  "chart": null,
  "crossFilters": [],
  "currency": null,
  "dashboardSetting": null,
  "description": "でんき契約ベースの契約者情報レポート",
  "detailColumns": [
    "Contractor_Information__c.Name",
    "Contractor_Information__c.smart_customer_id__c",
    "Electrical_Contract__c.Name",
    "Electrical_Contract__c.plan_code__c.Name",
    "Contractor_Information__c.parent_agency__c",
    "Contractor_Information__c.account__c",
    "Contractor_Information__c.sales_channel__c",
    "Contractor_Information__c.customer_type__c",
    "Contractor_Information__c.contractor_name__c",
    "Contractor_Information__c.contractor_name_kana__c",
    "Electrical_Contract__c.Comp_Before_Switch__c.Name",
    "Electrical_Contract__c.current_power_plan__c",
    "Electrical_Contract__c.supply_point_identification_no__c",
    "Electrical_Contract__c.customer_no__c",
    "Electrical_Contract__c.latest_billing_year_month__c",
    "Electrical_Contract__c.bill__c",
    "Electrical_Contract__c.power_usage_kwh__c",
    "Electrical_Contract__c.contract_amps__c",
    "Electrical_Contract__c.contract_kvc__c",
    "Electrical_Contract__c.billing_amount__c",
    "Electrical_Contract__c.discount_rate__c",
    "Contractor_Information__c.payment_type__c",
    "Electrical_Contract__c.place_name__c",
    "Contractor_Information__c.zip__c",
    "Contractor_Information__c.contractor_address__c",
    "Contractor_Information__c.request_date__c",
    "Contractor_Information__c.atokaku_call_status__c",
    "Electrical_Contract__c.contract_confirmation_call_ok_date__c",
    "Contractor_Information__c.latest_billing_month__c",
    "Contractor_Information__c.Latest_payment_meyhod__c",
    "Electrical_Contract__c.cancel_date__c",
    "Electrical_Contract__c.cancel_confirmed_date__c",
    "Electrical_Contract__c.cancellation_date__c",
    "Electrical_Contract__c.cancel_reason__c",
    "Electrical_Contract__c.use_place_zip__c",
    "Electrical_Contract__c.use_place_address_connect__c",
    "Electrical_Contract__c.use_place_name__c",
    "Electrical_Contract__c.use_place_name_kana__c",
    "Electrical_Contract__c.matching_result__c",
    "Electrical_Contract__c.switching_request_ok_date__c",
    "Electrical_Contract__c.scheduled_switching_date__c",
    "Contractor_Information__c.email__c",
    "Contractor_Information__c.business_sector__c",
    "Contractor_Information__c.business_sector_detail__c",
    "Contractor_Information__c.fact_clct_date__c",
    "Contractor_Information__c.representative_age__c",
    "Contractor_Information__c.representative_brth__c",
    "Contractor_Information__c.representative_country__c",
    "Contractor_Information__c.representative_name__c",
    "Contractor_Information__c.representative_name_kana__c",
    "Contractor_Information__c.pic_name__c",
    "Contractor_Information__c.pic_name_kana__c",
    "Contractor_Information__c.pic_tel__c",
    "Contractor_Information__c.shop_name__c",
    "Electrical_Contract__c.distinguish_place_tel__c",
    "Contractor_Information__c.tel1_connect__c",
    "Electrical_Contract__c.use_place_tel__c",
    "Contractor_Information__c.tel2_connect__c",
    "Contractor_Information__c.document_destination_name__c",
    "Contractor_Information__c.document_destination_address_connect__c",
    "Electrical_Contract__c.remarks1__c",
    "Electrical_Contract__c.remarks2__c",
    "Electrical_Contract__c.remarks3__c",
    "Contractor_Information__c.atokaku_comment__c",
    "Contractor_Information__c.claim_linking_no__c",
    "Contractor_Information__c.application_information__c.Name"
  ],
  "developerName": "CRM3",
  "division": null,
  "folderId": "00lQ9000000OIILIA4",
  "groupingsAcross": [],
  "groupingsDown": [],
  "hasDetailRows": true,
  "hasRecordCount": true,
  "historicalSnapshotDates": [],
  "id": "00OQ9000003Dq5VMAS",
  "name": "【でんき】☆CRM架電用☆　条件縛り",
  "presentationOptions": {
    "hasStackedSummaries": true
  },
  "reportBooleanFilter": null,
  "reportFilters": [
    {
      "column": "Electrical_Contract__c.cancel_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Electrical_Contract__c.cancel_reason__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Electrical_Contract__c.cancel_confirmed_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Electrical_Contract__c.cancel_cooperation_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Electrical_Contract__c.forced_termination_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Electrical_Contract__c.cancellation_confirmed_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Electrical_Contract__c.cancellation_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Electrical_Contract__c.Compulsory_cancellation_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Contractor_Information__c.parent_agency__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "株式会社アイステーション（管理）"
    },
    {
      "column": "Contractor_Information__c.parent_agency__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "株式会社アクセル（商品企画）"
    },
    {
      "column": "Contractor_Information__c.parent_agency__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "株式会社ネクシィーズ"
    },
    {
      "column": "Contractor_Information__c.account__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "株式会社ネクシィーズ"
    },
    {
      "column": "Contractor_Information__c.account__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "NUWORKS株式会社(t)"
    },
    {
      "column": "Contractor_Information__c.account__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "NUWORKS株式会社（テンポス）"
    },
    {
      "column": "Contractor_Information__c.account__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "株式会社come up"
    },
    {
      "column": "Contractor_Information__c.Latest_payment_meyhod__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "コンビニ"
    },
    {
      "column": "Contractor_Information__c.Call_FLG__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": ""
    },
    {
      "column": "Contractor_Information__c.parent_agency__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": "EPARK（管理）"
    },
    {
      "column": "Electrical_Contract__c.switching_request_ok_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "notEqual",
      "value": ""
    },
    {
      "column": "Electrical_Contract__c.scheduled_switching_date__c",
      "filterType": "fieldValue",
      "isRunPageEditable": true,
      "operator": "equals",
      "value": "2か月前"
    }
  ],
  "reportFormat": "TABULAR",
  "reportType": {
    "label": "契約者情報（TC）_でんき契約（TDC）",
    "type": "TC_TDC__c"
  },
  "scope": "organization",
  "showGrandTotal": true,
  "showSubtotals": true,
  "sortBy": [
    {
      "sortColumn": "Electrical_Contract__c.scheduled_switching_date__c",
      "sortOrder": "Desc"
    }
  ],
  "standardDateFilter": {
    "column": "Contractor_Information__c.CreatedDate",
    "durationValue": "CUSTOM",
    "endDate": null,
    "startDate": null
  },
  "standardFilters": null,
  "supportsRoleHierarchy": false,
  "userOrHierarchyFilterId": null,
  "detailColumnInfo": {
    "Contractor_Information__c.Name": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.Name",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.Name",
      "inactiveFilterValues": [],
      "isLookup": true,
      "label": "契約者コード",
      "uniqueCountable": true
    },
    "Contractor_Information__c.smart_customer_id__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.smart_customer_id__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.smart_customer_id__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "smart会員ID",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.Name": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.Name",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.Name",
      "inactiveFilterValues": [],
      "isLookup": true,
      "label": "電気契約ID",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.plan_code__c.Name": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.plan_code__c.Name",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.plan_code__c.Name",
      "inactiveFilterValues": [],
      "isLookup": true,
      "label": "プラン名: 表示プラン名",
      "uniqueCountable": true
    },
    "Contractor_Information__c.parent_agency__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.parent_agency__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.parent_agency__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "親代理店名",
      "uniqueCountable": true
    },
    "Contractor_Information__c.account__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.account__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.account__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "代理店名",
      "uniqueCountable": true
    },
    "Contractor_Information__c.sales_channel__c": {
      "dataType": "picklist",
      "entityColumnName": "Contractor_Information__c.sales_channel__c",
      "filterValues": [
        {
          "apiName": "テレマ",
          "label": "テレマ",
          "name": "テレマ"
        },
        {
          "apiName": "訪販",
          "label": "訪販",
          "name": "訪販"
        },
        {
          "apiName": "コラボ併売",
          "label": "コラボ併売",
          "name": "コラボ併売"
        },
        {
          "apiName": "飛び込み",
          "label": "飛び込み",
          "name": "飛び込み"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.sales_channel__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "販路",
      "uniqueCountable": true
    },
    "Contractor_Information__c.customer_type__c": {
      "dataType": "picklist",
      "entityColumnName": "Contractor_Information__c.customer_type__c",
      "filterValues": [
        {
          "apiName": "法人",
          "label": "法人",
          "name": "法人"
        },
        {
          "apiName": "屋号",
          "label": "屋号",
          "name": "屋号"
        },
        {
          "apiName": "個人（LP）",
          "label": "個人（LP）",
          "name": "個人（LP）"
        },
        {
          "apiName": "特商法対象",
          "label": "特商法対象",
          "name": "特商法対象"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.customer_type__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "顧客区分",
      "uniqueCountable": true
    },
    "Contractor_Information__c.contractor_name__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.contractor_name__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.contractor_name__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約者名",
      "uniqueCountable": true
    },
    "Contractor_Information__c.contractor_name_kana__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.contractor_name_kana__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.contractor_name_kana__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約者名_カナ",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.Comp_Before_Switch__c.Name": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.Comp_Before_Switch__c.Name",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.Comp_Before_Switch__c.Name",
      "inactiveFilterValues": [],
      "isLookup": true,
      "label": "切替前会社: 事業者名",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.current_power_plan__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.current_power_plan__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.current_power_plan__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "切替前会社プラン",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.supply_point_identification_no__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.supply_point_identification_no__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.supply_point_identification_no__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "【従量】供給地点特定番号（ハイフンなし）",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.customer_no__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.customer_no__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.customer_no__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "お客様番号（ハイフンなし）",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.latest_billing_year_month__c": {
      "dataType": "date",
      "entityColumnName": "Electrical_Contract__c.latest_billing_year_month__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.latest_billing_year_month__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "明細年月",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.bill__c": {
      "dataType": "picklist",
      "entityColumnName": "Electrical_Contract__c.bill__c",
      "filterValues": [
        {
          "apiName": "回収",
          "label": "回収",
          "name": "回収"
        },
        {
          "apiName": "手書き",
          "label": "手書き",
          "name": "手書き"
        },
        {
          "apiName": "明細なし（新店）",
          "label": "明細なし（新店）",
          "name": "明細なし（新店）"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.bill__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "明細",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.power_usage_kwh__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.power_usage_kwh__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.power_usage_kwh__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "電力使用量（kwh)",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.contract_amps__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.contract_amps__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.contract_amps__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約A数/Kv数",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.contract_kvc__c": {
      "dataType": "double",
      "entityColumnName": "Electrical_Contract__c.contract_kvc__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.contract_kvc__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約容量",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.billing_amount__c": {
      "dataType": "currency",
      "entityColumnName": "Electrical_Contract__c.billing_amount__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.billing_amount__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "明細料金",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.discount_rate__c": {
      "dataType": "picklist",
      "entityColumnName": "Electrical_Contract__c.discount_rate__c",
      "filterValues": [
        {
          "apiName": "1%",
          "label": "1%",
          "name": "1%"
        },
        {
          "apiName": "2%",
          "label": "2%",
          "name": "2%"
        },
        {
          "apiName": "3%",
          "label": "3%",
          "name": "3%"
        },
        {
          "apiName": "4%",
          "label": "4%",
          "name": "4%"
        },
        {
          "apiName": "5%",
          "label": "5%",
          "name": "5%"
        },
        {
          "apiName": "6%",
          "label": "6%",
          "name": "6%"
        },
        {
          "apiName": "7%",
          "label": "7%",
          "name": "7%"
        },
        {
          "apiName": "8%",
          "label": "8%",
          "name": "8%"
        },
        {
          "apiName": "9%",
          "label": "9%",
          "name": "9%"
        },
        {
          "apiName": "10%",
          "label": "10%",
          "name": "10%"
        },
        {
          "apiName": "11%",
          "label": "11%",
          "name": "11%"
        },
        {
          "apiName": "12%",
          "label": "12%",
          "name": "12%"
        },
        {
          "apiName": "13%",
          "label": "13%",
          "name": "13%"
        },
        {
          "apiName": "14%",
          "label": "14%",
          "name": "14%"
        },
        {
          "apiName": "15%",
          "label": "15%",
          "name": "15%"
        },
        {
          "apiName": "16%",
          "label": "16%",
          "name": "16%"
        },
        {
          "apiName": "17%",
          "label": "17%",
          "name": "17%"
        },
        {
          "apiName": "18%",
          "label": "18%",
          "name": "18%"
        },
        {
          "apiName": "19%",
          "label": "19%",
          "name": "19%"
        },
        {
          "apiName": "20%",
          "label": "20%",
          "name": "20%"
        },
        {
          "apiName": "21%",
          "label": "21%",
          "name": "21%"
        },
        {
          "apiName": "22%",
          "label": "22%",
          "name": "22%"
        },
        {
          "apiName": "23%",
          "label": "23%",
          "name": "23%"
        },
        {
          "apiName": "24%",
          "label": "24%",
          "name": "24%"
        },
        {
          "apiName": "25%",
          "label": "25%",
          "name": "25%"
        },
        {
          "apiName": "26%",
          "label": "26%",
          "name": "26%"
        },
        {
          "apiName": "27%",
          "label": "27%",
          "name": "27%"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.discount_rate__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "相対率",
      "uniqueCountable": true
    },
    "Contractor_Information__c.payment_type__c": {
      "dataType": "picklist",
      "entityColumnName": "Contractor_Information__c.payment_type__c",
      "filterValues": [
        {
          "apiName": "口座振替（個人名義）",
          "label": "口座振替（個人名義）",
          "name": "口座振替（個人名義）"
        },
        {
          "apiName": "口座振替（法人名義）",
          "label": "口座振替（法人名義）",
          "name": "口座振替（法人名義）"
        },
        {
          "apiName": "クレジットカード",
          "label": "クレジットカード",
          "name": "クレジットカード"
        },
        {
          "apiName": "アクセル請求",
          "label": "アクセル請求",
          "name": "アクセル請求"
        },
        {
          "apiName": "コンビニ支払い",
          "label": "コンビニ支払い",
          "name": "コンビニ支払い"
        },
        {
          "apiName": "既存請求合算",
          "label": "既存請求合算",
          "name": "既存請求合算"
        },
        {
          "apiName": "OEM",
          "label": "OEM",
          "name": "OEM"
        },
        {
          "apiName": "SBSおまとめ",
          "label": "SBSおまとめ",
          "name": "SBSおまとめ"
        },
        {
          "apiName": "債権譲渡",
          "label": "債権譲渡",
          "name": "債権譲渡"
        },
        {
          "apiName": "請求書払い（入札案件用）",
          "label": "請求書払い（入札案件用）",
          "name": "請求書払い（入札案件用）"
        },
        {
          "apiName": "請求書払い（高圧電力用）",
          "label": "請求書払い（高圧電力用）",
          "name": "請求書払い（高圧電力用）"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.payment_type__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "登録時支払方法",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.place_name__c": {
      "dataType": "picklist",
      "entityColumnName": "Electrical_Contract__c.place_name__c",
      "filterValues": [
        {
          "apiName": "関東",
          "label": "関東",
          "name": "関東"
        },
        {
          "apiName": "関西",
          "label": "関西",
          "name": "関西"
        },
        {
          "apiName": "中部",
          "label": "中部",
          "name": "中部"
        },
        {
          "apiName": "九州",
          "label": "九州",
          "name": "九州"
        },
        {
          "apiName": "北海道",
          "label": "北海道",
          "name": "北海道"
        },
        {
          "apiName": "東北",
          "label": "東北",
          "name": "東北"
        },
        {
          "apiName": "中国",
          "label": "中国",
          "name": "中国"
        },
        {
          "apiName": "四国",
          "label": "四国",
          "name": "四国"
        },
        {
          "apiName": "北陸",
          "label": "北陸",
          "name": "北陸"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.place_name__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "地域",
      "uniqueCountable": true
    },
    "Contractor_Information__c.zip__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.zip__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.zip__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約者住所_郵便番号",
      "uniqueCountable": true
    },
    "Contractor_Information__c.contractor_address__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.contractor_address__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.contractor_address__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約者住所",
      "uniqueCountable": true
    },
    "Contractor_Information__c.request_date__c": {
      "dataType": "date",
      "entityColumnName": "Contractor_Information__c.request_date__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.request_date__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "申込日",
      "uniqueCountable": true
    },
    "Contractor_Information__c.atokaku_call_status__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.atokaku_call_status__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.atokaku_call_status__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契確コールステータス",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.contract_confirmation_call_ok_date__c": {
      "dataType": "date",
      "entityColumnName": "Electrical_Contract__c.contract_confirmation_call_ok_date__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.contract_confirmation_call_ok_date__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約確認コールOK日",
      "uniqueCountable": true
    },
    "Contractor_Information__c.latest_billing_month__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.latest_billing_month__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.latest_billing_month__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "最新請求月",
      "uniqueCountable": true
    },
    "Contractor_Information__c.Latest_payment_meyhod__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.Latest_payment_meyhod__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.Latest_payment_meyhod__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "最新支払方法",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.cancel_date__c": {
      "dataType": "date",
      "entityColumnName": "Electrical_Contract__c.cancel_date__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.cancel_date__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "キャンセル日",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.cancel_confirmed_date__c": {
      "dataType": "date",
      "entityColumnName": "Electrical_Contract__c.cancel_confirmed_date__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.cancel_confirmed_date__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "キャンセル受領日",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.cancellation_date__c": {
      "dataType": "date",
      "entityColumnName": "Electrical_Contract__c.cancellation_date__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.cancellation_date__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "解約日",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.cancel_reason__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.cancel_reason__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.cancel_reason__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "解約・キャンセル理由",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.use_place_zip__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.use_place_zip__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.use_place_zip__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "使用場所_郵便番号",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.use_place_address_connect__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.use_place_address_connect__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.use_place_address_connect__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "使用場所住所",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.use_place_name__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.use_place_name__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.use_place_name__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "明細名義名",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.use_place_name_kana__c": {
      "dataType": "string",
      "entityColumnName": "Electrical_Contract__c.use_place_name_kana__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.use_place_name_kana__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "明細名義カナ",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.matching_result__c": {
      "dataType": "picklist",
      "entityColumnName": "Electrical_Contract__c.matching_result__c",
      "filterValues": [
        {
          "apiName": "OK（完了）",
          "label": "OK（完了）",
          "name": "OK（完了）"
        },
        {
          "apiName": "OK※エラーあり",
          "label": "OK※エラーあり",
          "name": "OK※エラーあり"
        },
        {
          "apiName": "NG（顧客確認中）",
          "label": "NG（顧客確認中）",
          "name": "NG（顧客確認中）"
        },
        {
          "apiName": "処理中",
          "label": "処理中",
          "name": "処理中"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.matching_result__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "マッチング処理結果",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.switching_request_ok_date__c": {
      "dataType": "date",
      "entityColumnName": "Electrical_Contract__c.switching_request_ok_date__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.switching_request_ok_date__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "マッチングOK日",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.scheduled_switching_date__c": {
      "dataType": "date",
      "entityColumnName": "Electrical_Contract__c.scheduled_switching_date__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.scheduled_switching_date__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "スイッチング予定日",
      "uniqueCountable": true
    },
    "Contractor_Information__c.email__c": {
      "dataType": "email",
      "entityColumnName": "Contractor_Information__c.email__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.email__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "email①",
      "uniqueCountable": true
    },
    "Contractor_Information__c.business_sector__c": {
      "dataType": "picklist",
      "entityColumnName": "Contractor_Information__c.business_sector__c",
      "filterValues": [
        {
          "apiName": "飲食業",
          "label": "飲食業",
          "name": "飲食業"
        },
        {
          "apiName": "サービス業",
          "label": "サービス業",
          "name": "サービス業"
        },
        {
          "apiName": "小売業",
          "label": "小売業",
          "name": "小売業"
        },
        {
          "apiName": "製造業",
          "label": "製造業",
          "name": "製造業"
        },
        {
          "apiName": "建設業",
          "label": "建設業",
          "name": "建設業"
        },
        {
          "apiName": "運輸業",
          "label": "運輸業",
          "name": "運輸業"
        },
        {
          "apiName": "不動産業",
          "label": "不動産業",
          "name": "不動産業"
        },
        {
          "apiName": "卸売業",
          "label": "卸売業",
          "name": "卸売業"
        },
        {
          "apiName": "金融業",
          "label": "金融業",
          "name": "金融業"
        },
        {
          "apiName": "介護・医療",
          "label": "介護・医療",
          "name": "介護・医療"
        },
        {
          "apiName": "工場",
          "label": "工場",
          "name": "工場"
        },
        {
          "apiName": "ホテル・旅館",
          "label": "ホテル・旅館",
          "name": "ホテル・旅館"
        },
        {
          "apiName": "事務所",
          "label": "事務所",
          "name": "事務所"
        },
        {
          "apiName": "農家・農園",
          "label": "農家・農園",
          "name": "農家・農園"
        },
        {
          "apiName": "自宅兼事業所",
          "label": "自宅兼事業所",
          "name": "自宅兼事業所"
        },
        {
          "apiName": "その他",
          "label": "その他",
          "name": "その他"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.business_sector__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "業種",
      "uniqueCountable": true
    },
    "Contractor_Information__c.business_sector_detail__c": {
      "dataType": "picklist",
      "entityColumnName": "Contractor_Information__c.business_sector_detail__c",
      "filterValues": [
        {
          "apiName": "居酒屋",
          "label": "居酒屋",
          "name": "居酒屋"
        },
        {
          "apiName": "焼肉店",
          "label": "焼肉店",
          "name": "焼肉店"
        },
        {
          "apiName": "ラーメン店",
          "label": "ラーメン店",
          "name": "ラーメン店"
        },
        {
          "apiName": "食堂、レストラン、定食屋",
          "label": "食堂、レストラン、定食屋",
          "name": "食堂、レストラン、定食屋"
        },
        {
          "apiName": "中華料理店",
          "label": "中華料理店",
          "name": "中華料理店"
        },
        {
          "apiName": "韓国料理店",
          "label": "韓国料理店",
          "name": "韓国料理店"
        },
        {
          "apiName": "カレー専門店",
          "label": "カレー専門店",
          "name": "カレー専門店"
        },
        {
          "apiName": "インド料理店",
          "label": "インド料理店",
          "name": "インド料理店"
        },
        {
          "apiName": "タイ・ベトナム料理店",
          "label": "タイ・ベトナム料理店",
          "name": "タイ・ベトナム料理店"
        },
        {
          "apiName": "イタリア料理店",
          "label": "イタリア料理店",
          "name": "イタリア料理店"
        },
        {
          "apiName": "フランス料理店",
          "label": "フランス料理店",
          "name": "フランス料理店"
        },
        {
          "apiName": "スペイン料理店",
          "label": "スペイン料理店",
          "name": "スペイン料理店"
        },
        {
          "apiName": "その他多国籍料理店",
          "label": "その他多国籍料理店",
          "name": "その他多国籍料理店"
        },
        {
          "apiName": "日本料理店（割烹・会席）",
          "label": "日本料理店（割烹・会席）",
          "name": "日本料理店（割烹・会席）"
        },
        {
          "apiName": "日本料理店（鍋）",
          "label": "日本料理店（鍋）",
          "name": "日本料理店（鍋）"
        },
        {
          "apiName": "そば、うどん店",
          "label": "そば、うどん店",
          "name": "そば、うどん店"
        },
        {
          "apiName": "すし店",
          "label": "すし店",
          "name": "すし店"
        },
        {
          "apiName": "お好み焼、焼きそば、たこ焼、鉄板焼き店",
          "label": "お好み焼、焼きそば、たこ焼、鉄板焼き店",
          "name": "お好み焼、焼きそば、たこ焼、鉄板焼き店"
        },
        {
          "apiName": "カフェ、喫茶店",
          "label": "カフェ、喫茶店",
          "name": "カフェ、喫茶店"
        },
        {
          "apiName": "FC店",
          "label": "FC店",
          "name": "FC店"
        },
        {
          "apiName": "唐揚げ専門店",
          "label": "唐揚げ専門店",
          "name": "唐揚げ専門店"
        },
        {
          "apiName": "ハンバーガー店",
          "label": "ハンバーガー店",
          "name": "ハンバーガー店"
        },
        {
          "apiName": "バー、バル",
          "label": "バー、バル",
          "name": "バー、バル"
        },
        {
          "apiName": "弁当屋",
          "label": "弁当屋",
          "name": "弁当屋"
        },
        {
          "apiName": "タピオカ店",
          "label": "タピオカ店",
          "name": "タピオカ店"
        },
        {
          "apiName": "その他（座席のある料理店）",
          "label": "その他（座席のある料理店）",
          "name": "その他（座席のある料理店）"
        },
        {
          "apiName": "その他（座席のない料理店）",
          "label": "その他（座席のない料理店）",
          "name": "その他（座席のない料理店）"
        },
        {
          "apiName": "美容室",
          "label": "美容室",
          "name": "美容室"
        },
        {
          "apiName": "理容室",
          "label": "理容室",
          "name": "理容室"
        },
        {
          "apiName": "ネイルサロン",
          "label": "ネイルサロン",
          "name": "ネイルサロン"
        },
        {
          "apiName": "ジム",
          "label": "ジム",
          "name": "ジム"
        },
        {
          "apiName": "エステ",
          "label": "エステ",
          "name": "エステ"
        },
        {
          "apiName": "介護",
          "label": "介護",
          "name": "介護"
        },
        {
          "apiName": "その他",
          "label": "その他",
          "name": "その他"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.business_sector_detail__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "業種詳細",
      "uniqueCountable": true
    },
    "Contractor_Information__c.fact_clct_date__c": {
      "dataType": "date",
      "entityColumnName": "Contractor_Information__c.fact_clct_date__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.fact_clct_date__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "ファクタ回収日",
      "uniqueCountable": true
    },
    "Contractor_Information__c.representative_age__c": {
      "dataType": "double",
      "entityColumnName": "Contractor_Information__c.representative_age__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.representative_age__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "代表者年齢",
      "uniqueCountable": true
    },
    "Contractor_Information__c.representative_brth__c": {
      "dataType": "date",
      "entityColumnName": "Contractor_Information__c.representative_brth__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.representative_brth__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "代表者生年月日",
      "uniqueCountable": true
    },
    "Contractor_Information__c.representative_country__c": {
      "dataType": "picklist",
      "entityColumnName": "Contractor_Information__c.representative_country__c",
      "filterValues": [
        {
          "apiName": "日本",
          "label": "日本",
          "name": "日本"
        },
        {
          "apiName": "外国人",
          "label": "外国人",
          "name": "外国人"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.representative_country__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "代表者国籍",
      "uniqueCountable": true
    },
    "Contractor_Information__c.representative_name__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.representative_name__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.representative_name__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "代表者名",
      "uniqueCountable": true
    },
    "Contractor_Information__c.representative_name_kana__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.representative_name_kana__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.representative_name_kana__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "代表者名_カナ",
      "uniqueCountable": true
    },
    "Contractor_Information__c.pic_name__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.pic_name__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.pic_name__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "担当者名",
      "uniqueCountable": true
    },
    "Contractor_Information__c.pic_name_kana__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.pic_name_kana__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.pic_name_kana__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "担当者名_カナ",
      "uniqueCountable": true
    },
    "Contractor_Information__c.pic_tel__c": {
      "dataType": "phone",
      "entityColumnName": "Contractor_Information__c.pic_tel__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.pic_tel__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "担当者電話番号",
      "uniqueCountable": true
    },
    "Contractor_Information__c.shop_name__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.shop_name__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.shop_name__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "支店・店舗・施設名",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.distinguish_place_tel__c": {
      "dataType": "picklist",
      "entityColumnName": "Electrical_Contract__c.distinguish_place_tel__c",
      "filterValues": [
        {
          "apiName": "1.自宅",
          "label": "1.自宅",
          "name": "1.自宅"
        },
        {
          "apiName": "2.携帯",
          "label": "2.携帯",
          "name": "2.携帯"
        },
        {
          "apiName": "3.家族・親族",
          "label": "3.家族・親族",
          "name": "3.家族・親族"
        },
        {
          "apiName": "4.配偶者",
          "label": "4.配偶者",
          "name": "4.配偶者"
        },
        {
          "apiName": "5.家主・管理人",
          "label": "5.家主・管理人",
          "name": "5.家主・管理人"
        },
        {
          "apiName": "6.事務所",
          "label": "6.事務所",
          "name": "6.事務所"
        },
        {
          "apiName": "7.店舗",
          "label": "7.店舗",
          "name": "7.店舗"
        },
        {
          "apiName": "8.本社",
          "label": "8.本社",
          "name": "8.本社"
        },
        {
          "apiName": "9.その他",
          "label": "9.その他",
          "name": "9.その他"
        }
      ],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.distinguish_place_tel__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "電話番号区分",
      "uniqueCountable": true
    },
    "Contractor_Information__c.tel1_connect__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.tel1_connect__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.tel1_connect__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約者_電話番号①",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.use_place_tel__c": {
      "dataType": "phone",
      "entityColumnName": "Electrical_Contract__c.use_place_tel__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.use_place_tel__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "使用場所_電話番号",
      "uniqueCountable": true
    },
    "Contractor_Information__c.tel2_connect__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.tel2_connect__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.tel2_connect__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契約者_電話番号②",
      "uniqueCountable": true
    },
    "Contractor_Information__c.document_destination_name__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.document_destination_name__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.document_destination_name__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "書面郵送先送付宛名",
      "uniqueCountable": true
    },
    "Contractor_Information__c.document_destination_address_connect__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.document_destination_address_connect__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.document_destination_address_connect__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "書面郵送先住所",
      "uniqueCountable": true
    },
    "Electrical_Contract__c.remarks1__c": {
      "dataType": "textarea",
      "entityColumnName": "Electrical_Contract__c.remarks1__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.remarks1__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "電気備考①",
      "uniqueCountable": false
    },
    "Electrical_Contract__c.remarks2__c": {
      "dataType": "textarea",
      "entityColumnName": "Electrical_Contract__c.remarks2__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.remarks2__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "電気備考②",
      "uniqueCountable": false
    },
    "Electrical_Contract__c.remarks3__c": {
      "dataType": "textarea",
      "entityColumnName": "Electrical_Contract__c.remarks3__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Electrical_Contract__c.remarks3__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "電気備考③",
      "uniqueCountable": false
    },
    "Contractor_Information__c.atokaku_comment__c": {
      "dataType": "textarea",
      "entityColumnName": "Contractor_Information__c.atokaku_comment__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.atokaku_comment__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "契確コールコメント",
      "uniqueCountable": false
    },
    "Contractor_Information__c.claim_linking_no__c": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.claim_linking_no__c",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.claim_linking_no__c",
      "inactiveFilterValues": [],
      "isLookup": false,
      "label": "請求紐づけ番号※申込コード",
      "uniqueCountable": true
    },
    "Contractor_Information__c.application_information__c.Name": {
      "dataType": "string",
      "entityColumnName": "Contractor_Information__c.application_information__c.Name",
      "filterValues": [],
      "filterable": true,
      "fullyQualifiedName": "Contractor_Information__c.application_information__c.Name",
      "inactiveFilterValues": [],
      "isLookup": true,
      "label": "申込コード: 申込コード",
      "uniqueCountable": true
    }
  }
}

"""
Salesforce Bulk API 2.0 を使用してレポートデータを取得する
自動生成されたファイル
"""

import requests
import time
import csv
import io
import json
from datetime import datetime
import os
import re


class SalesforceBulkQuery:
    def __init__(self, config):
        # Salesforce関係
        self.sf_username = config.sf_username
        self.sf_password = config.sf_password
        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.sf_access_token_URL = config.sf_access_token_URL
        self.api_version = config.api_version
        
        # SOQL取得
        self.soql = config.soql

        # レポートメタデータ
        self.report_meta = config.report_meta

        # output の csv のパス
        now = datetime.now()
        year = now.strftime("%Y年")          # 例: 2025
        month = now.strftime("%m月")         # 例: 01
        file_name = now.strftime("%m月%d日.csv")  # 例: 01月12日.csv

        base_dir = config.sf_folder_base_path
        year_dir = os.path.join(base_dir, year)
        month_dir = os.path.join(year_dir, month)

        # フォルダを自動作成
        os.makedirs(month_dir, exist_ok=True)

        # 完全パス
        self.output_csv_path = os.path.join(month_dir, file_name)

    def execute(self):
        """
        実際の抽出処理
        Salesforceのアクセストークンを取得して、Salesforceのレポートを取得
        """
        # 認証
        access_token, instance_url = self.authenticate_salesforce()
        print(f"[INFO] Connected to {instance_url}")

        # クエリ実行
        results = self.run_bulk_query(instance_url, access_token)
        print(f"[INFO] 結果を {self.output_csv_path} に保存しました。")
        
        return results

    def authenticate_salesforce(self):
        """
        Salesforce OAuth2認証を行う

        Returns:
            (access_token, instance_url)
        """
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.sf_username,
            "password": self.sf_password
        }

        response = requests.post(self.sf_access_token_URL, data=payload)
        if response.status_code != 200:
            print("[ERROR] Salesforce authentication failed:")
            print(response.text)
            raise Exception(f"Salesforce authentication failed ({response.status_code})")

        data = response.json()
        return data["access_token"], data["instance_url"]

    def run_bulk_query(self, instance_url, access_token) -> list:
        """
        Bulk API 2.0でSOQLクエリを実行し、結果をリストで返す

        Args:
            instance_url: SalesforceインスタンスURL
            access_token: アクセストークン

        Returns:
            CSVデータを2次元リストとして返す
        """
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        base_url = f"{instance_url}/services/data/v{self.api_version}/jobs/query"

        # 1. ジョブ作成
        payload = {
            "operation": "query",
            "query": self.soql,
            "contentType": "CSV"
        }

        job_res = requests.post(base_url, headers=headers, json=payload)

        if not job_res.ok:
            print("[ERROR] Job creation failed")
            print("Status:", job_res.status_code)
            try:
                error_text = json.dumps(job_res.json(), indent=2, ensure_ascii=False)
                print(error_text)
            except Exception:
                print(job_res.text)
            job_res.raise_for_status()

        job_id = job_res.json()["id"]
        print(f"[INFO] Job created: {job_id}")

        # 2. ジョブ完了待ち
        while True:
            status_res = requests.get(f"{base_url}/{job_id}", headers=headers)
            status_res.raise_for_status()
            state = status_res.json()["state"]
            print(f"[INFO] Job state: {state}")
            if state in ("JobComplete", "Failed", "Aborted"):
                break
            time.sleep(5)

        if state != "JobComplete":
            print(f"[ERROR] Job ended with state: {state}")
            print(status_res.text)
            raise Exception("Bulk query job failed.")

        # 3. 結果CSVダウンロード
        result_res = requests.get(f"{base_url}/{job_id}/results", headers=headers)
        result_res.raise_for_status()
        decoded = result_res.content.decode("utf-8")
        all_rows = list(csv.reader(io.StringIO(decoded)))

        print(f"[INFO] Retrieved {len(all_rows)} rows (including header)")

        # 4. CSV保存（パスが指定されている場合）
        self.save_to_csv(all_rows, self.output_csv_path)
        
        return all_rows

    def save_to_csv(self, data, output_path):
        """
        データをCSVファイルに保存する
        REPORT_METAが定義されていれば、カラム名を日本語に変換する

        Args:
            data: 2次元リストのデータ
            output_path: 出力ファイルパス
        """
        # report_metaを使用してカラム名を日本語に変換
        if len(data) > 0 and self.report_meta is not None:
            try:
                base_object = self._extract_base_object_from_soql(self.soql)
                label_map = self._build_column_label_map(self.report_meta, base_object)
                data[0] = self._convert_headers_to_labels(data[0], label_map)
                print(f"[INFO] カラム名を日本語に変換しました")
            except Exception as e:
                print(f"[WARN] カラム名変換に失敗しました: {e}")

        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"[INFO] Saved to {output_path}")

    def _build_column_label_map(self, report_meta: dict, base_object: str = None) -> dict:
        """
        レポート定義からAPI名→日本語ラベルのマッピングを構築する
        キーは小文字に正規化される（Bulk APIが小文字で返すため）

        Args:
            report_meta: レポートメタデータ（detailColumnInfoを含む）
            base_object: FROM句のベースオブジェクト名（例: "OptionObject__c"）

        Returns:
            API名（小文字）をキー、日本語ラベルを値とする辞書
        """
        label_map = {}
        detail_column_info = report_meta.get("detailColumnInfo", {})

        for api_name, info in detail_column_info.items():
            label = info.get("label", api_name)
            # API名からBulk APIのカラム名形式に変換
            parts = api_name.split(".")
            if len(parts) >= 2:
                first_object = parts[0]  # 最初のオブジェクト名
                field_parts = parts[1:]

                # ベースオブジェクト以外のオブジェクトからのフィールドは親参照として扱う
                if base_object and first_object != base_object:
                    # 親オブジェクトへの参照: ObjectName__c → objectname__r
                    parent_ref = first_object.replace("__c", "__r").lower()
                    # __c を __r に変換（最後の項目以外）
                    converted_parts = []
                    for i, part in enumerate(field_parts):
                        if i < len(field_parts) - 1 and part.endswith("__c"):
                            converted_parts.append(part.replace("__c", "__r"))
                        else:
                            converted_parts.append(part)
                    bulk_column_name = parent_ref + "." + ".".join(converted_parts)
                else:
                    # ベースオブジェクトのフィールド: 最初のオブジェクト名を除去
                    converted_parts = []
                    for i, part in enumerate(field_parts):
                        if i < len(field_parts) - 1 and part.endswith("__c"):
                            converted_parts.append(part.replace("__c", "__r"))
                        else:
                            converted_parts.append(part)
                    bulk_column_name = ".".join(converted_parts)

                # 小文字に正規化してマッピング
                label_map[bulk_column_name.lower()] = label
            else:
                label_map[api_name.lower()] = label

        return label_map

    def _convert_headers_to_labels(self, headers_row: list, label_map: dict) -> list:
        """
        CSVヘッダー行をAPI名から日本語ラベルに変換する

        Args:
            headers_row: CSVのヘッダー行（API名のリスト）
            label_map: API名（小文字）→ラベルのマッピング

        Returns:
            日本語ラベルに変換されたヘッダー行
        """
        return [label_map.get(h.lower(), h) for h in headers_row]

    def _extract_base_object_from_soql(self, soql: str) -> str:
        """
        SOQLからFROM句のベースオブジェクト名を抽出する

        Args:
            soql: SOQLクエリ文字列

        Returns:
            ベースオブジェクト名（例: "OptionObject__c"）
        """
        match = re.search(r'\bFROM\s+(\w+)', soql, re.IGNORECASE)
        if match:
            return match.group(1)
        return None


# 使用例
if __name__ == "__main__":
    # 設定クラス（Config）を作成する
    class Config:
        def __init__(self):
            # Salesforce接続情報
            self.sf_username = "your_username@example.com"
            self.sf_password = "your_password"
            self.client_id = "your_client_id"
            self.client_secret = "your_client_secret"
            self.sf_access_token_URL = "https://login.salesforce.com/services/oauth2/token"
            self.api_version = "62.0"

            # SOQL（このファイルではSOQL_QUERYを使用）
            self.soql = SOQL_QUERY

            # レポートメタデータ（このファイルではREPORT_METAを使用）
            self.report_meta = REPORT_META

            # CSV出力先のベースパス
            self.sf_folder_base_path = "./output"

    # Configインスタンスを作成
    config = Config()

    # SalesforceBulkQueryを実行
    sf_query = SalesforceBulkQuery(config)

    # クエリ実行
    results = sf_query.execute()
    print(f"[SUCCESS] 取得完了: {len(results)}行")
