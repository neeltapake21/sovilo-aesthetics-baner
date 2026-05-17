const reviews = [
  {
    id: 1,
    name: "Priya M.",
    rating: 5,
    comment: "Amazing experience with Dr. Suryawanshi. My skin has never looked better!",
    service: "Hydrafacial",
  },
  {
    id: 2,
    name: "Rahul S.",
    rating: 5,
    comment: "PRP treatment showed visible results within 3 sessions. Highly recommend.",
    service: "PRP Hair Treatment",
  },
  {
    id: 3,
    name: "Sneha K.",
    rating: 5,
    comment: "The laser hair removal was painless and effective. Great clinic!",
    service: "Laser Hair Removal",
  },
];

export default function handler(req, res) {
  res.status(200).json({ reviews });
}
