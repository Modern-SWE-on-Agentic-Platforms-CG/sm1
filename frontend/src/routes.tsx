import { Routes, Route } from 'react-router-dom'
import ProtectedRoute from '@/components/ProtectedRoute'
import RoleRoute from '@/components/RoleRoute'

import LoginPage from '@/pages/LoginPage'
import SelectRolePage from '@/pages/SelectRolePage'
import DashboardPage from '@/pages/DashboardPage'
import TodoListPage from '@/pages/TodoListPage'
import PanelRegistrationPage from '@/pages/PanelRegistrationPage'
import CandidateListPage from '@/pages/CandidateListPage'
import CandidateDetailPage from '@/pages/CandidateDetailPage'
import BookingFormPage from '@/pages/BookingFormPage'
import UploadPage from '@/pages/UploadPage'
import FeedbackFormPage from '@/pages/FeedbackFormPage'
import WebFeedbackPage from '@/pages/WebFeedbackPage'
import WorkflowPage from '@/pages/WorkflowPage'
import WorkflowInfoPage from '@/pages/WorkflowInfoPage'
import JoiningBonusPage from '@/pages/JoiningBonusPage'
import JBCandidatesPage from '@/pages/JBCandidatesPage'
import AdministrationPage from '@/pages/AdministrationPage'
import MasterDataPage from '@/pages/MasterDataPage'
import SelectRejectPage from '@/pages/SelectRejectPage'
import DateOfJoiningPage from '@/pages/DateOfJoiningPage'
import UpdateSkillPage from '@/pages/UpdateSkillPage'
import CandidateApprovalDataPage from '@/pages/CandidateApprovalDataPage'
import FeedbackFormReportPage from '@/pages/FeedbackFormReportPage'
import DashboardReportsPage from '@/pages/DashboardReportsPage'
import LineChartPage from '@/pages/LineChartPage'
import TrendChartPage from '@/pages/TrendChartPage'
import InterviewDataPage from '@/pages/InterviewDataPage'
import StatusInsightsPage from '@/pages/StatusInsightsPage'
import ChannelInsightsPage from '@/pages/ChannelInsightsPage'
import ArcDeviationPage from '@/pages/ArcDeviationPage'
import RejectionReportPage from '@/pages/RejectionReportPage'
import L2ReportPage from '@/pages/L2ReportPage'
import L2AgingPage from '@/pages/L2AgingPage'
import WeekendDrivePage from '@/pages/WeekendDrivePage'
import ImportWeekendDrivePage from '@/pages/ImportWeekendDrivePage'
import ReferralProtectedRoute from '@/components/ReferralProtectedRoute'
import CandidateReferralPage from '@/pages/CandidateReferralPage'
import CandidateReferralDetailsPage from '@/pages/CandidateReferralDetailsPage'
import ReferralFormPage from '@/pages/ReferralFormPage'
import ReferralRegisterPage from '@/pages/ReferralRegisterPage'
import RefCandidateDetailsPage from '@/pages/RefCandidateDetailsPage'
import ReferralReportsByBUPage from '@/pages/ReferralReportsByBUPage'
import ReferralReportsByAccountPage from '@/pages/ReferralReportsByAccountPage'
import DemandSupplyPage from '@/pages/DemandSupplyPage'
import PanelInsightsPage from '@/pages/PanelInsightsPage'
import ChangeRolesPage from '@/pages/ChangeRolesPage'

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected — any authenticated user */}
      <Route path="/selectrole" element={
        <ProtectedRoute><SelectRolePage /></ProtectedRoute>
      } />

      {/* Interviewer */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Interviewer']}>
            <DashboardPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Recruiter / PMO */}
      <Route path="/todolist" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Recruiter', 'PMO', 'RecruiterLead', 'Interviewer']}>
            <TodoListPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Admin */}
      <Route path="/register-panel" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Admin']}>
            <PanelRegistrationPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Candidate management */}
      <Route path="/candidate-details" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Recruiter', 'PMO', 'Admin', 'RecruiterLead']}>
            <CandidateListPage />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/candidate-details/:id" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Recruiter', 'PMO', 'Admin', 'RecruiterLead', 'Interviewer']}>
            <CandidateDetailPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Booking */}
      <Route path="/booking-form" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Recruiter', 'PMO', 'Admin']}>
            <BookingFormPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Upload */}
      <Route path="/upload" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Recruiter', 'PMO', 'Admin', 'SAP Recruiter']}>
            <UploadPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Feedback */}      <Route path="/feedback/:bookingId" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Interviewer']}>
            <FeedbackFormPage />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/webFeedback/:bookingId" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Interviewer']}>
            <WebFeedbackPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Workflow */}
      <Route path="/work-flow" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['TowerLead', 'SLBULead', 'NALead', 'RecruiterLead', 'Admin']}>
            <WorkflowPage />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/work-flow-info" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['TowerLead', 'SLBULead', 'NALead', 'RecruiterLead', 'Admin', 'Recruiter']}>
            <WorkflowInfoPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Joining Bonus */}
      <Route path="/joiningbonus" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['RecruiterLead', 'Admin', 'BUAdmin']}>
            <JoiningBonusPage />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/jbcandidates" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Recruiter', 'RecruiterLead', 'Admin']}>
            <JBCandidatesPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Administration */}
      <Route path="/administration" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Admin']}>
            <AdministrationPage />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/master-data" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['BUAdmin', 'PracticeAdmin', 'Admin']}>
            <MasterDataPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Documents */}
      <Route path="/select-reject" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Recruiter', 'RecruiterLead', 'Admin']}>
            <SelectRejectPage />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/dateofjoining" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['PMO', 'Admin']}>
            <DateOfJoiningPage />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/update-skill" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['Recruiter', 'RecruiterLead', 'Admin']}>
            <UpdateSkillPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Reports */}
      <Route path="/candidate-approval-data" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['PMO', 'Admin', 'RecruiterLead']}>
            <CandidateApprovalDataPage />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/feedback-form-report" element={
        <ProtectedRoute>
          <RoleRoute allowedRoles={['PMO', 'Admin', 'RecruiterLead', 'Interviewer']}>
            <FeedbackFormReportPage />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Analytics */}
      <Route path="/dashboard-reports" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'Recruiter', 'RecruiterLead', 'PMO']}><DashboardReportsPage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/line-chart" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'RecruiterLead', 'PMO']}><LineChartPage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/trend-chart" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'RecruiterLead', 'PMO']}><TrendChartPage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/interview-data" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'RecruiterLead', 'PMO', 'Interviewer']}><InterviewDataPage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/status-insights" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'RecruiterLead', 'PMO']}><StatusInsightsPage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/channel-insights" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'RecruiterLead', 'PMO']}><ChannelInsightsPage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/arc-deviation" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'RecruiterLead']}><ArcDeviationPage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/rejection-report" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'RecruiterLead', 'PMO']}><RejectionReportPage /></RoleRoute></ProtectedRoute>
      } />

      {/* L2 */}
      <Route path="/l2-report" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Recruiter', 'RecruiterLead', 'Admin']}><L2ReportPage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/l2-aging" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Recruiter', 'RecruiterLead', 'Admin']}><L2AgingPage /></RoleRoute></ProtectedRoute>
      } />

      {/* Weekend Drive */}
      <Route path="/weekend-drive" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Recruiter', 'RecruiterLead', 'Admin']}><WeekendDrivePage /></RoleRoute></ProtectedRoute>
      } />
      <Route path="/import-weekend-drive" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Recruiter', 'RecruiterLead', 'Admin']}><ImportWeekendDrivePage /></RoleRoute></ProtectedRoute>
      } />

      {/* Referral Portal — public */}
      <Route path="/referral" element={<ReferralRegisterPage />} />
      <Route path="/referral-form" element={<ReferralFormPage />} />

      {/* Referral Portal — protected */}
      <Route path="/referral-candidates" element={
        <ReferralProtectedRoute><CandidateReferralPage /></ReferralProtectedRoute>
      } />
      <Route path="/referral-details/:id" element={
        <ReferralProtectedRoute><CandidateReferralDetailsPage /></ReferralProtectedRoute>
      } />
      <Route path="/ref-candidate-details/:id" element={
        <ReferralProtectedRoute><RefCandidateDetailsPage /></ReferralProtectedRoute>
      } />
      <Route path="/referral-reports-bu" element={
        <ReferralProtectedRoute><ReferralReportsByBUPage /></ReferralProtectedRoute>
      } />
      <Route path="/referral-reports-account" element={
        <ReferralProtectedRoute><ReferralReportsByAccountPage /></ReferralProtectedRoute>
      } />

      {/* Supply / Demand */}
      <Route path="/demand-supply" element={
        <ProtectedRoute><RoleRoute allowedRoles={['PMO', 'Admin', 'RecruiterLead']}><DemandSupplyPage /></RoleRoute></ProtectedRoute>
      } />

      {/* Panel Insights */}
      <Route path="/panel-insights" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin', 'RecruiterLead']}><PanelInsightsPage /></RoleRoute></ProtectedRoute>
      } />

      {/* Change Roles */}
      <Route path="/change-roles" element={
        <ProtectedRoute><RoleRoute allowedRoles={['Admin']}><ChangeRolesPage /></RoleRoute></ProtectedRoute>
      } />

      {/* Fallback — MUST be last */}
      <Route path="*" element={<LoginPage />} />
    </Routes>
  )
}
