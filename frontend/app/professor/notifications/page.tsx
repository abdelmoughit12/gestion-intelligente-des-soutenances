'use client'

import React from 'react';
import ProfessorLayout from '@/components/shared/ProfessorLayout';
import withAuth from '@/components/withAuth';
import { UserRole } from '@/types/soutenance';

// Créez ici un composant pour afficher la liste complète des notifications
const NotificationListComponent = () => {
    // Ceci sera un 'use client' component plus tard pour la gestion des clics "Marquer comme lu"
    return (
        <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-2xl font-bold mb-4">Historique des Notifications</h2>
            {/* Implémenter ici la liste des notifications (Tâche 4.4) */}
            <p className="text-gray-600">Liste complète de toutes les alertes et affectations.</p>
        </div>
    );
};

function ProfessorNotificationsPage() {
    // Simulation du nombre de notifs non lues pour le layout
    const unreadCount = 2;

    return (
        <ProfessorLayout pageTitle="Mes Notifications" unreadCount={unreadCount}>
            <NotificationListComponent />
        </ProfessorLayout>
    );
}

export default withAuth(ProfessorNotificationsPage, UserRole.Professor);