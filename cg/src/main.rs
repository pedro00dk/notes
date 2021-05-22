mod util;
use util::Vx;

fn main() {
    let v = util::V3::<f32> {
        x: 0.0,
        y: 0.0,
        z: 0.0,
    };
    let u = util::V3::of(0.0f32);
    println!("Hello, world! {:?}", v);
}
