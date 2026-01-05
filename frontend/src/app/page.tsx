import Yolo from "../components/Yolo";


export default function Home() {
  return (
    <>
      <main className="font-mono flex flex-col justify-center items-center  w-screen">
        <h1 className="m-5 text-xl font-bold">Rubik's Cube Detector + Solver</h1>
        <Yolo />
        <footer>
          Created By @JimWid
        </footer>
      </main>
    </>
  );
}