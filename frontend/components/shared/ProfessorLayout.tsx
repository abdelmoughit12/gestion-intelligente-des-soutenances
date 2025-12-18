// frontend/components/shared/ProfessorLayout.tsx
import React from 'react';


interface ProfessorLayoutProps {
  children: React.ReactNode;
  pageTitle: string;
  unreadCount: number; 
}

export default function ProfessorLayout({ children, pageTitle, unreadCount }: ProfessorLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header pageTitle={pageTitle} unreadCount={unreadCount} />
      
      <main className="flex-grow max-w-7xl mx-auto w-full py-8 px-4 sm:px-6 lg:px-8">
        {children}
      </main>
      
      <Footer />
    </div>
  );
}

// Composants de base (doivent être créés dans shared/)
// Note: Le code du Header incluant la cloche est dans notre réponse précédente.
const Header = ({ pageTitle, unreadCount }: { pageTitle: string, unreadCount: number }) => (
    // Code du Header (utiliser la structure Next.js/Tailwind/Lucide)
    <header className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
            {/* ... Titre/Logo ... */}
        </div>
    </header>
);

const Footer = () => (
    <footer className="bg-white border-t mt-10">
        {/* ... Contenu simple du Footer ... */}
    </footer>
);