use crate::math::VR;

pub struct Camera {
    pub position: VR<f32, 4>,
    pub direction: VR<f32, 4>,
}
