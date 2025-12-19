import MultiPageDashboard from '@/components/MultiPageDashboard'
import withAuth from '@/components/withAuth'
import { UserRole } from '@/types/soutenance';

function StudentPage() {
    return <MultiPageDashboard />
}

const AuthStudentPage = withAuth(StudentPage, UserRole.Student);

export default AuthStudentPage;
