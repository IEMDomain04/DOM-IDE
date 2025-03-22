"use client";

import React from "react";
import { useRouter } from "next/navigation";

interface Keyword {
  name: string;
  description: string;
}

const keywords: Keyword[] = [
  { name: "domain", description: "Serves as the main function of the program." },
  { name: "null", description: "Represents no value." },
  { name: "int, float, string, bool", description: "Declare variables corresponding to their data type." },
  { name: "restrict", description: "Declare variables with immutable values." },
  { name: "invoke", description: "Displays arguments to console." },
  { name: "capture", description: "Ask the user for an input before proceeding to the next line." },
  { name: "true", description: "Represents the truth value of an expression. It is non-zero." },
  { name: "false", description: "Represents the false value, which is zero." },
  { name: "vow", description: "Executes code if a condition is true." },
  { name: "else vow", description: "Used to extend a vow statement, executes if a condition is true." },
  { name: "else", description: "Executes the code if previous vow statements are false." },
  { name: "boogie", description: "Evaluates an expression, executes matching case." },
  { name: "woogie", description: "Conditional statement of boogie statements." },
  { name: "default", description: "Performs this block of code if no conditions were met in the boogie statement." },
  { name: "cycle", description: "Iterates a block of code." },
  { name: "sustain", description: "Loops while a condition is true." },
  { name: "perform sustain", description: "Code block is executed at least once." },
  { name: "dismiss", description: "A control statement used to abruptly exit out of a loop statement." },
  { name: "hop", description: "Used to skip the current iteration of a loop and proceed with the next iteration." },
  { name: "recall", description: "Used to exit from a function/curse and optionally send a value back to the caller." },
  { name: "cleave", description: "Takes a starting index and number of elements to be returned by the function." },
  { name: "dismantle", description: "Splits string or sentences and converts it to an array." },
  { name: "len()", description: "Returns the length of a string or clan." },
  { name: "curse", description: "Creates a user-defined function that executes a block of code when called." },
];

const Overview: React.FC = () => {
  const router = useRouter();

  return (
    <div className="p-6 font-sans bg-dark-background">
      {/* Floating Button */}
      <button
        onClick={() => router.push("/.")}
        className="fixed bottom-5 left-5 w-14 h-14 bg-gray-800 text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-300 hover:bg-gray-700 hover:scale-110 active:bg-red-500"
      >
        <h1 className="font-jujutsu">Back</h1>
      </button>

      {/* Title */}
      <h1 className="text-2xl font-bold">Overview of the DOM Compiler Programming Language</h1>
      <p className="mt-2 text-gray-700">
        This is a brief overview of the reserved words used in the DOM Compiler language and their functions.
      </p>

      {/* Keyword Table */}
      <table className="w-full mt-6 border-collapse border border-gray-500">
        <thead>
          <tr className="bg-gray-900 text-white">
            <th className="p-3 border border-gray-700">Keyword</th>
            <th className="p-3 border border-gray-700">Function</th>
          </tr>
        </thead>
        <tbody>
          {keywords.map((keyword, index) => (
            <tr key={index} className="border border-gray-500">
              <td className="p-3 font-semibold border border-gray-700">{keyword.name}</td>
              <td className="p-3 border border-gray-700">{keyword.description}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h1 className="mt-10 text-center">"Enjoy Programming!" BSCS 3 - 1 Group 1</h1>
    </div>
  );
};

export default Overview;
