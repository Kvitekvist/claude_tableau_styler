"""
Dashboard Rebuilder

Takes an existing Tableau workbook and creates a new dashboard
with professional layout following design guidelines.
"""

from lxml import etree
import copy
from parser.workbook import Workbook
from dashboard.layout_builder import LayoutBuilder


class DashboardRebuilder:
    """Rebuilds dashboards with modern professional layouts"""

    def __init__(self):
        self.layout_builder = LayoutBuilder()

    def rebuild_hjem_dashboard(self, workbook: Workbook) -> Workbook:
        """
        Rebuild the Hjem.no dashboard with proper structure

        Current structure (from screenshot analysis):
        - 3 KPIs: # active ads, # Retailers, % on FINN
        - 1 Pie chart: Objects on FINN
        - 1 Area chart: Daily Active (PRIMARY - trend over time)
        - 1 Bar chart: Ads by Agency Group
        - 1 Table: All Ads listed

        New structure (following guidelines):
        ------------------------------------------------
        Dashboard Title
        ------------------------------------------------
        Filter Bar (Agency Group, ON_FINN)
        ------------------------------------------------
        KPI 1    |    KPI 2    |    KPI 3
        ------------------------------------------------
        Primary Trend Chart (Daily Active)
        ------------------------------------------------
        Bar Chart    |    Pie Chart
        ------------------------------------------------
        Detail Table
        ------------------------------------------------
        """
        # Create deep copy to avoid modifying original
        rebuilt = copy.deepcopy(workbook)

        # Find the Hjem.no dashboard
        hjem_dashboard = None
        hjem_index = None
        for i, dashboard in enumerate(rebuilt.dashboards):
            if dashboard.name == 'Hjem.no':
                hjem_dashboard = dashboard
                hjem_index = i
                break

        if not hjem_dashboard:
            raise ValueError("Hjem.no dashboard not found")

        # Create new dashboard with proper layout
        new_dashboard_elem = self.layout_builder.create_modern_dashboard(
            title="Norwegian Real Estate Competitor Analysis",
            subtitle="Track new competitor 'Hjem' property listings in Norway",
            kpi_worksheets=[
                'Hjem.no # active ads',
                'Hjem.no # Retailers',
                'Hjem.no % on FINN'
            ],
            primary_chart='Hjem.no Daily Active',
            supporting_charts=[
                'Hjem.no Ads by Agency Group',
                'Hjem.no Pie Chart'
            ],
            table_worksheet='Hjem.no All Ads listed',
            filters=None  # Add later if needed
        )

        # Find dashboards element in XML
        dashboards_elem = rebuilt.xml_root.find('dashboards')
        if dashboards_elem is not None:
            # Find and remove old Hjem.no dashboard
            for dash in dashboards_elem.findall('dashboard'):
                if dash.get('name') == 'Hjem.no':
                    dashboards_elem.remove(dash)

            # Add new dashboard
            dashboards_elem.append(new_dashboard_elem)

        # Update workbook dashboard objects
        # Note: We keep the Dashboard object but update its XML element
        if hjem_index is not None and hjem_index < len(rebuilt.dashboards):
            rebuilt.dashboards[hjem_index].xml_element = new_dashboard_elem
            rebuilt.dashboards[hjem_index].name = 'Hjem.no'

        return rebuilt
