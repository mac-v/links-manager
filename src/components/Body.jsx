import Container from "react-bootstrap/esm/Container";
import Sidebar from "./Sidebar";
import Stack from "react-bootstrap/Stack"

export default function Body({sidebar, children}) {
    return (
        <Container>
            <Stack direction="horizontal" className="Body">
                {sidebar && <Sidebar />}
                <Container className="Content">
                    {children}
                </Container>
            </Stack>
        </Container>
    )
}