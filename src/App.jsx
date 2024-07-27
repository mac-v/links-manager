import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import SettingsPage from './pages/SettingsPage';
import LinksPage from './pages/LinksPage';
import LoginPage from './pages/LoginPage';
import UserPage from './pages/UserPage';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';


export default function App() {
    return (
      <Container fluid className="App">
        <BrowserRouter>
          <Header />
          <Routes>
            <Route path="/links" element={<LinksPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="*" element={<Navigate to="/links" />} />
            <Route path="/user/:username" element={<UserPage />} />
          </Routes>
        </BrowserRouter>
      </Container>
    );
  }