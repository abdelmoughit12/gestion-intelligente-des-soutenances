import { api } from './api';

export interface PendingStudent {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  cni: string;
  phone: string;
  creation_date: string;
}

export interface ProfessorCreateData {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  password: string;
  specialty: string;
}

export const getPendingStudents = async (): Promise<PendingStudent[]> => {
  try {
    const response = await api.get('/api/v1/manager/pending-students');
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch pending students');
  }
};

export const approveStudent = async (userId: number): Promise<any> => {
  try {
    const response = await api.patch(`/api/v1/manager/pending-students/${userId}/approve`);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to approve student');
  }
};

export const rejectStudent = async (userId: number): Promise<void> => {
  try {
    await api.delete(`/api/v1/manager/pending-students/${userId}/reject`);
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to reject student');
  }
};

export const addProfessor = async (data: ProfessorCreateData): Promise<any> => {
  try {
    const response = await api.post('/api/v1/manager/professors', data);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to add professor');
  }
};
