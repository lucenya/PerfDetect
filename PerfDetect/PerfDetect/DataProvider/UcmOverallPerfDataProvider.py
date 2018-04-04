from . import SqlConnector
import pandas as pd
import numpy as np

ucmServiceMappingData = np.array(
   [["Advertiser Accounts",	                        "/AdvertiserAccounts",	        "AccountsGrid.LoadData",	                                        "UCM-A"],
    ["Account Opportunities ",	                    "/AccountOpportunities",	    "OpportunitiesGrid.LoadData",	                                    "UCM-A"],
    ["Bob Advertiser",	                            "/Advertisers",	                "AdvertisersGrid.LoadData",	                                        "UCM-A"],
    ["Bob Accounts",	                            "/Accounts",	                "AccountsGrid.LoadData",	                                        "UCM-A"],
    ["Search Advertisers",	                        "/Search",	                    "SearchAdvertisersGrid.LoadData",	                                "UCM-A"],
    ["Search Accounts",	                            "/Search",	                    "SearchAccountsGrid.LoadData",	                                    "UCM-A"],
    ["Bob Agencies",	                            "/Agencies",	                "AgenciesGrid.LoadData",	                                        "UCM-A"],
    ["Advertiser Opportunities",	                "/AdvertiserOpportunities",	    "OpportunitiesGrid.LoadData",	                                    "UCM-A"],
    ["Advertiser Alerts",	                        "/AdvertiserAlerts",	        "AlertsGrid.LoadData",	                                            "UCM-A"],
    ["Support",	                                    "/Support",	                    "SupportGrid.LoadData",	                                            "UCM-A"],
    ["Job Queue",	                                "/JobQueue",	                "JobQueueGrid.LoadData",	                                        "UCM-A"],
    ["Label Accounts",	                            "/LabelAccounts",	            "AccountsGrid.LoadData",	                                        "UCM-A"],
    ["Label Advertisers",	                        "/LabelAdvertisers",	        "AdvertisersGrid.LoadData",	                                        "UCM-A"],
    ["Label Agencies",	                            "/LabelAgencies",	            "AgenciesGrid.LoadData",	                                        "UCM-A"],
    ["Catch And Release Customers",	                "/CatchAndReleaseManager",	    "CatchAndReleaseCustomersGrid.LoadData",	                        "UCM-A"],
    ["Catch And Release Team",	                    "/CatchAndReleaseManager",	    "CatchAndReleaseTeamGrid.LoadData",	                                "UCM-A"],
    ["Account Feature Adoption",	                "/AccountFeatureAdoption",	    "FeatureAdoptionGrid.LoadData",	                                    "UCM-A"],
    ["Opportunities",	                            "/Opportunities",	            "OpportunitiesGrid.LoadData",	                                    "UCM-A"],
    ["Alerts",	                                    "/Alerts",	                    "AlertsGrid.LoadData",	                                            "UCM-A"],
    ["My Queue",	                                "/AgentsQueue/Advertiser",	    "AdvertisersGrid.LoadData",	                                        "UCM-A"],
    ["Agency Accounts",	                            "/AgencyAccounts",	            "AccountsGrid.LoadData",	                                        "UCM-A"],
    ["Advertiser Pilots",	                        "/AdvertiserPilots",	        "CustomerPilotGrid.LoadData",	                                    "UCM-A"],
    ["Advertiser Engagement History",	            "/AdvertiserEngagementHistory",	"EngagementHistoryGrid.LoadData",	                                "UCM-A"],
    ["Account Competitor Group",	                "/AccountCompetitorGroup",	    "CompetitorGroupGrid.LoadData",	                                    "UCM-A"],
    ["Advertiser Competitor Group",	                "/AdvertiserCompetitorGroup",	"CompetitorGroupGrid.LoadData",	                                    "UCM-A"],
    ["Account Alerts",	                            "/AccountAlerts",	            "AlertsGrid.LoadData",	                                            "UCM-A"],
    ["Advertiser Contacts",	                        "/AdvertiserContacts",	        "ContactDetailsGrid.LoadData",	                                    "UCM-A"],
    ["My Tasks",	                                "/MyTasks",	                    "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Label tasks",	                                "/LabelTasks",	                "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Bob tasks",	                                "/Tasks",	                    "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Advertiser tasks",	                        "/AdvertiserTasks",	            "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Agency Tasks",	                            "/AgencyTasks",	                "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Account Tasks",	                            "/AccountTasks",	            "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Agents Queue Tasks",	                        "/AgentsQueue/Tasks",	        "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Job Queue",	                                "/JobQueue",	                "JobQueueGrid.LoadData",	                                        "UCM-A"],
    ["Label Accounts",	                            "/LabelAccounts",	            "AccountsGrid.LoadData",	                                        "UCM-A"],
    ["Label Advertisers",	                        "/LabelAdvertisers",	        "AdvertisersGrid.LoadData",	                                        "UCM-A"],
    ["Label Agencies",	                            "/LabelAgencies",	            "AgenciesGrid.LoadData",	                                        "UCM-A"],
    ["Catch And Release Customers",	                "/CatchAndReleaseManager",	    "CatchAndReleaseCustomersGrid.LoadData",	                        "UCM-A"],
    ["Catch And Release Team",	                    "/CatchAndReleaseManager",	    "CatchAndReleaseTeamGrid.LoadData",	                                "UCM-A"],
    ["Account Feature Adoption",	                "/AccountFeatureAdoption",	    "FeatureAdoptionGrid.LoadData",	                                    "UCM-A"],
    ["Opportunities",	                            "/Opportunities",	            "OpportunitiesGrid.LoadData",	                                    "UCM-A"],
    ["Alerts",	                                    "/Alerts",	                    "AlertsGrid.LoadData",	                                            "UCM-A"],
    ["My Queue",	                                "/AgentsQueue/Advertiser",	    "AdvertisersGrid.LoadData",	                                        "UCM-A"],
    ["Agency Accounts",	                            "/AgencyAccounts",	            "AccountsGrid.LoadData",	                                        "UCM-A"],
    ["Advertiser Pilots",	                        "/AdvertiserPilots",	        "CustomerPilotGrid.LoadData",	                                    "UCM-A"],
    ["Advertiser Engagement History",	            "/AdvertiserEngagementHistory",	"EngagementHistoryGrid.LoadData",	                                "UCM-A"],
    ["Account Competitor Group",	                "/AccountCompetitorGroup",	    "CompetitorGroupGrid.LoadData",	                                    "UCM-A"],
    ["Advertiser Competitor Group",	                "/AdvertiserCompetitorGroup",	"CompetitorGroupGrid.LoadData",	                                    "UCM-A"],
    ["Account Alerts",	                            "/AccountAlerts",	            "AlertsGrid.LoadData",	                                            "UCM-A"],
    ["Advertiser Contacts",	                        "/AdvertiserContacts",	        "ContactDetailsGrid.LoadData",	                                    "UCM-A"],
    ["My Tasks",	                                "/MyTasks",	                    "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Label tasks",	                                "/LabelTasks",	                "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Bob tasks",	                                "/Tasks",	                    "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Advertiser tasks",	                        "/AdvertiserTasks",	            "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Agency Tasks",	                            "/AgencyTasks",	                "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Account Tasks",	                            "/AccountTasks",	            "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Agents Queue Tasks",	                        "/AgentsQueue/Tasks",	        "TasksGridName.LoadData",	                                        "UCM-A"],
    ["Attainment Summary",	                        "/Attainment",	                "AttainmentSummaryGrid.LoadData",	                                "UCM-B"],
    ["Teams Attiainment Summary",	                "/TeamsAttainment",	            "TeamsAttainmentSummaryGrid.LoadData",	                            "UCM-B"],
    ["Attainment Details",	                        "/Attainment",	                "AttainmentDetailsGrid.LoadData",	                                "UCM-B"],
    ["Teams Attainment Team",	                    "/TeamsAttainment",	            "TeamsAttainmentTeamGrid.LoadData",	                                "UCM-B"],
    ["Teams Attainment Details",	                "/TeamsAttainment",	            "TeamsAttainmentDetailsGrid.LoadData",	                            "UCM-B"],
    ["Details advertisers",	                        "/Attainment",	                "AttainmentDetailsGrid.LoadData-GroupByAdvertisers",	            "UCM-B"],
    ["Details agencies",	                        "/Attainment",	                "AttainmentDetailsGrid.LoadData-GroupByAgencies",	                "UCM-B"],
    ["Details accounts",	                        "/Attainment",	                "AttainmentDetailsGrid.LoadData-GroupByAccounts",	                "UCM-B"],
    ["Details assignment type",	                    "/Attainment",	                "AttainmentDetailsGrid.LoadData-GroupByAssignmentType",	            "UCM-B"],
    ["Teams Details advertisers",	                "/TeamsAttainment",	            "AttainmentDetailsGrid.LoadData-GroupByAdvertisers",	            "UCM-B"],
    ["Teams Details agencies",	                    "/TeamsAttainment",	            "AttainmentDetailsGrid.LoadData-GroupByAgencies",	                "UCM-B"],
    ["Teams Details accounts",	                    "/TeamsAttainment",	            "AttainmentDetailsGrid.LoadData-GroupByAccounts",	                "UCM-B"],
    ["Teams Details assignment type",	            "/TeamsAttainment",	            "AttainmentDetailsGrid.LoadData-GroupByAssignmentType",	            "UCM-B"],
    ["Teams Team FlatStructure",	                "/TeamsAttainment",	            "TeamsAttainmentTeamGrid.LoadData-GroupByFlatStructure",	        "UCM-B"],
    ["Teams Team OrgStructure",	                    "/TeamsAttainment",	            "TeamsAttainmentTeamGrid.LoadData-GroupByOrganizationalStructure",	"UCM-B"],
    ["Change Management Assingment",	            "/BookAssignments",	            "ChangeManagementAssignmentGrid.LoadData",	                        "UCM-C"],
    ["Agency Timeline ",	                        "/AccountHistory",	            "AgencyTimelineGrid.LoadData",	                                    "UCM-C"],
    ["Team Member Association",	                    "/TeamManagement",	            "TeamMemberAssociationGrid.LoadData",	                            "UCM-C"],
    ["Sales Ex Changes",	                        "/ChangeManagement",	        "SalesExChangesGrid.LoadData",	                                    "UCM-C"],
    ["Account History",	                            "/ClientAssignment",	        "AccountHistoryGrid.LoadData",	                                    "UCM-C"],
    ["Ticketing Team Queue",	                    "/TeamQueue",	                "TicketsViewGrid.LoadData",	                                        "UCM-T"],
    ["Ticket Communication",	                    "/EditTicket",	                "TicketCommunicationDetailsTabGrid.LoadData",	                    "UCM-T"],
    ["Ticket Customer Details",	                    "/EditTicket",	                "TicketCustomerDetailsGrid.LoadData",	                            "UCM-T"],
    ["Ticket Attachment",	                        "/EditTicket",	                "TicketAttachmentGrid.LoadData",	                                "UCM-T"],
    ["Ticket Stakeholder Details",	                "/EditTicket",	                "TicketStakeholderDetailsGrid.LoadData",	                        "UCM-T"],
    ["Ticket Edit History",	                        "/EditTicket",	                "TicketEditHistoryDetailsGrid.LoadData",	                        "UCM-T"],
    ["Ticket Links",	                            "/EditTicket",	                "TicketLinksGrid.LoadData",	                                        "UCM-T"],
    ["VTeams",	                                    "/MyTeams",	                    "VTeamsGrid.LoadData",	                                            "UCM-T"],
    ["Ticket Administration Team Action Mapping",	"/MyTeams",	                    "TicketAdministrationTeamActionMappingGrid.LoadData",	            "UCM-T"],
    ["Book Of Tickets",	                            "/BookOfTickets",	            "TicketsViewGrid.LoadData",	                                        "UCM-T"],
    ["Ticketing Team Queue Auto Refresh ",	        "/TeamQueue",	                "TicketsViewGrid.AutoRefresh.LoadData",	                            "UCM-T"],
    ["Book Of Tickets",	                            "/BookOfTickets",	            "TicketsViewGrid.LoadData",	                                        "UCM-T"],
    ["Ticketing Team Queue Auto Refresh ",	        "/TeamQueue",	                "TicketsViewGrid.AutoRefresh.LoadData",	                            "UCM-T"],
    ["Ticket Read Email",	                        "/EditTicket",	                "GetEmailMessage",	                                                "UCM-T"]])

columns = ["service", "pageRoute", "recordingName", "workSpace"]
UcmServiceMapping = pd.DataFrame(ucmServiceMappingData, columns=columns)

WorkSpace = ["UCM-A", "UCM-B", "UCM-C", "UCM-T"]

class UcmOverallPerfDataProvider(object):
    def __init__(self):
        self.sqlConnect = SqlConnector.SqlConnector()

    def GetWorkSpaceList(self):
        return WorkSpace

    def GetPerfData(self, service):
        sqlQuery = self.getExternalServiceCallSQLQuery(service)
        return self.sqlConnect.GetDataAsDataFrame(sqlQuery, SqlConnector.overallColumnNameList)

    def GetDetectedServiceList(self, workSpace):
        services = UcmServiceMapping[UcmServiceMapping.workSpace == workSpace].service
        return services.tolist()

    def getExternalServiceCallSQLQuery(self, service):
        item = UcmServiceMapping[UcmServiceMapping.service == service]
        columnNames = ""
        for name in SqlConnector.overallColumnNameList:
            columnNames = columnNames + "[" + name + "],"
        columnNames = columnNames[0:len(columnNames)-1]
        sqlQuery = "SELECT TOP(120) " + columnNames + \
                "FROM [Kusto].[PercentilePerformanceTrend_Day] " + \
                "where userAlias='All' and " + \
                "pageRoute='" + item.pageRoute.tolist()[0] + "' and " +\
                "recordingName='" + item.recordingName.tolist()[0] + "' and " +\
                "workspace='" + item.workSpace.tolist()[0] + "' and " +\
                "DATENAME(dw, startDayHour)<>'Saturday' and DATENAME(dw,startDayHour)<>'Sunday' " + \
                "order by startDayHour desc"
        return sqlQuery
