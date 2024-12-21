
export default function Topnav() {
  return (
    <>
      <div>
        {/* Top Nav */}
        <div className="flex justify-center space-x-96 px-2 py-4 bg-purple-950">

          {/* Logo and Title of Compiler */}
          <div className="flex gap-x-2 items-center ">
            <img src="/dom-icon.svg" width={20} height={20} alt="Dom icon" />
            <h1>DOM COMPILER</h1>
          </div>

          {/* Saves and runs */}
          <div className="flex gap-x-12">
            <div className="flex gap-x-2 px-2 py-2 rounded cursor-pointer hover:bg-purple-500/20">
              <img src={`/saveas-icon.svg`} alt="" />
              <h1>SAVE AS</h1>
            </div>

            <div className="flex gap-x-2 px-2 py-2 rounded cursor-pointer hover:bg-purple-500/20">
              <img src={`/open-icon.svg`} alt="" />
              <h1>OPEN</h1>
            </div>

            <div className="flex gap-x-2 px-2 py-2 rounded cursor-pointer hover:bg-purple-500/20">
              <img src={`/run-icon.svg`} alt="" />
              <h1>RUN</h1>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
