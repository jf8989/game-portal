import type { NextApiRequest, NextApiResponse } from "next";
import axios from "axios";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === "POST") {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/guess/",
        req.body
      );
      res.status(200).json(response.data);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Error submitting guess" });
    }
  } else {
    res.setHeader("Allow", ["POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
