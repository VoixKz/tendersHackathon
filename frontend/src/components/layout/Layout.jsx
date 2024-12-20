import { Outlet } from 'react-router-dom';
import './Layout.css'

const Layout = () => {
    return(
        <main>
            <header>

            </header>

            <Outlet />

            <footer>
                
            </footer>
        </main>
    )
}

export default Layout;